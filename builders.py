import asyncio
import logging
import os
from datetime import datetime
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# استيراد الموديلات
from models import ScheduledPost

# إعداد الرابط الآمن للمجدول 🛡️
db_url = os.getenv("DATABASE_URL", "")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(url=db_url)
AsyncSessionLocal = async_sessionmaker(engine)

# --- القائمة الرئيسية (Reply Keyboard) ---
def main_menu_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="➕ ربط قناة"), KeyboardButton(text="📊 خطتي الحالية"))
    builder.row(KeyboardButton(text="📝 جدولة منشور"), KeyboardButton(text="⬆️ ترقية الاشتراك"))
    builder.row(KeyboardButton(text="🛠 الدعم الفني"), KeyboardButton(text="📖 شرح الاستخدام"))
    builder.row(KeyboardButton(text="💳 الدفع والاشتراك"))
    return builder.as_markup(resize_keyboard=True, input_field_placeholder="اختر من القائمة...")

# --- أزرار الدعم (Inline - فتح مباشر) ---
def support_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🛠 الدعم الفني", url="https://t.me"))
    builder.row(InlineKeyboardButton(text="📢 قناة التحديثات", url="https://t.me"))
    return builder.as_markup()

# --- محرك الجدولة والنشر والحذف التلقائي ---
async def start_scheduler(bot: Bot):
    logging.info("🚀 محرك الجدولة بدأ العمل...")
    while True:
        try:
            async with AsyncSessionLocal() as session:
                now = datetime.now()
                # 1. فحص المنشورات للنشر
                stmt = select(ScheduledPost).where(ScheduledPost.post_date <= now, ScheduledPost.is_sent == False)
                result = await session.execute(stmt)
                for post in result.scalars().all():
                    try:
                        msg = await bot.copy_message(chat_id=post.channel_id, from_chat_id=post.owner_id, message_id=post.message_id)
                        post.sent_message_id = msg.message_id
                        post.is_sent = True
                        await session.commit()
                        logging.info(f"✅ تم النشر في القناة: {post.channel_id}")
                    except Exception as e: logging.error(f"Error Posting: {e}")

                # 2. فحص المنشورات للحذف
                stmt_del = select(ScheduledPost).where(ScheduledPost.delete_date <= now, ScheduledPost.is_sent == True, ScheduledPost.is_deleted == False)
                result_del = await session.execute(stmt_del)
                for post in result_del.scalars().all():
                    try:
                        await bot.delete_message(chat_id=post.channel_id, message_id=post.sent_message_id)
                        post.is_deleted = True
                        await session.commit()
                        logging.info(f"🗑 تم الحذف من القناة: {post.channel_id}")
                    except Exception as e: logging.error(f"Error Deleting: {e}")
        except Exception as e:
            logging.error(f"Scheduler Loop Error: {e}")
        await asyncio.sleep(60)

# دوال إضافية
def admin_panel_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="👥 عرض المستخدمين"), KeyboardButton(text="📢 إذاعة عامة"))
    builder.row(KeyboardButton(text="🔙 العودة للقائمة الرئيسية"))
    return builder.as_markup(resize_keyboard=True)

def plans_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="🥈 Pro", callback_data="plan_pro")
    builder.adjust(1)
    return builder.as_markup()
    
