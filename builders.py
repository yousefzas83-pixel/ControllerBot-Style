import asyncio
import logging
import os
from datetime import datetime
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# استيراد الموديل
from models import ScheduledPost

# --- محاولة جلب الرابط بأمان ---
db_url = os.getenv("DATABASE_URL")

if not db_url:
    logging.error("❌ خطأ حرج: لم يتم العثور على DATABASE_URL في متغيرات البيئة!")
    # سنضع رابطاً وهمياً مؤقتاً لكي لا ينهار البوت أثناء التشغيل (فقط ليتجاوز مرحلة التشغيل)
    db_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
else:
    # تصحيح البادئة
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# إنشاء المحرك
engine = create_async_engine(url=db_url)
AsyncSessionLocal = async_sessionmaker(engine)

# --- الدوال (تأكد من بقائها كما هي) ---
def main_menu_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="➕ ربط قناة"), KeyboardButton(text="📊 خطتي الحالية"))
    builder.row(KeyboardButton(text="📝 جدولة منشور"), KeyboardButton(text="⬆️ ترقية الاشتراك"))
    builder.row(KeyboardButton(text="💳 الدفع والاشتراك"), KeyboardButton(text="📖 شرح الاستخدام"))
    builder.row(KeyboardButton(text="🛠 الدعم الفني"))
    return builder.as_markup(resize_keyboard=True)

def support_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🛠 الدعم الفني", url="https://t.me"))
    builder.row(InlineKeyboardButton(text="📢 قناة التحديثات", url="https://t.me"))
    return builder.as_markup()

def admin_panel_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="👥 عرض المستخدمين"), KeyboardButton(text="📢 إذاعة عامة"))
    builder.row(KeyboardButton(text="🔙 العودة للقائمة الرئيسية"))
    return builder.as_markup(resize_keyboard=True)

def plans_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🥈 Pro", callback_data="plan_pro")
    builder.adjust(1)
    return builder.as_markup()

# --- محرك الجدولة ---
async def start_scheduler(bot: Bot):
    # إذا كان الرابط وهمياً، لا تشغل المجدول لكي لا يسبب أخطاء
    if "localhost" in db_url:
        logging.warning("⚠️ محرك الجدولة معطل لأن DATABASE_URL غير مضبوط بشكل صحيح.")
        return

    logging.info("🚀 محرك الجدولة بدأ العمل...")
    while True:
        try:
            async with AsyncSessionLocal() as session:
                now = datetime.now()
                # (باقي كود النشر والحذف كما هو...)
                stmt = select(ScheduledPost).where(ScheduledPost.post_date <= now, ScheduledPost.is_sent == False)
                result = await session.execute(stmt)
                for post in result.scalars().all():
                    try:
                        msg = await bot.copy_message(chat_id=post.channel_id, from_chat_id=post.owner_id, message_id=post.message_id)
                        post.sent_message_id = msg.message_id
                        post.is_sent = True
                        await session.commit()
                    except Exception as e: logging.error(f"نشر خاطئ: {e}")
        except Exception as e:
            logging.error(f"خطأ في المجدول: {e}")
        await asyncio.sleep(60)
    
