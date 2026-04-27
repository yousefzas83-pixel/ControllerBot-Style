import asyncio
import logging
from datetime import datetime
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot
from sqlalchemy import select

# استيراد مكونات قاعدة البيانات
from models import ScheduledPost
from database import SessionLocal

# --- 1. القائمة الرئيسية (Reply Keyboard) ---
def main_menu_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    
    # تنسيق الأزرار: زرين بجانب بعضهما
    builder.row(KeyboardButton(text="➕ ربط قناة"), KeyboardButton(text="📊 خطتي الحالية"))
    builder.row(KeyboardButton(text="📝 جدولة منشور"), KeyboardButton(text="⬆️ ترقية الاشتراك"))
    builder.row(KeyboardButton(text="💳 الدفع والاشتراك"), KeyboardButton(text="📖 شرح الاستخدام"))
    # زر وحيد تحتهم
    builder.row(KeyboardButton(text="🛠 الدعم الفني"))
    
    return builder.as_markup(resize_keyboard=True, input_field_placeholder="اختر من القائمة...")

# --- 2. أزرار الدعم (Inline Keyboard - فتح مباشر) ---
def support_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    # الروابط تفتح مباشرة داخل تلجرام كما طلبت
    builder.row(InlineKeyboardButton(text="🛠 الدعم الفني", url="https://t.me"))
    builder.row(InlineKeyboardButton(text="📢 قناة التحديثات", url="https://t.me"))
    return builder.as_markup()

# --- 3. أزرار اختيار الخطط ---
def plans_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🥈 الخطة الاحترافية (Pro)", callback_data="plan_pro"))
    builder.row(InlineKeyboardButton(text="🥇 الخطة الذهبية (Gold)", callback_data="plan_gold"))
    builder.row(InlineKeyboardButton(text="❌ إلغاء", callback_data="cancel_action"))
    return builder.as_markup()

# --- 4. لوحة الإدارة (للأدمن) ---
def admin_panel_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="👥 عرض المستخدمين"), KeyboardButton(text="📢 إذاعة عامة"))
    builder.row(KeyboardButton(text="🔙 العودة للقائمة الرئيسية"))
    return builder.as_markup(resize_keyboard=True)

# --- 5. محرك الجدولة والنشر والحذف التلقائي ---
async def start_scheduler(bot: Bot):
    """المحرك الذي يفحص قاعدة البيانات كل دقيقة للنشر أو الحذف"""
    logging.info("🚀 محرك الجدولة بدأ العمل...")
    
    while True:
        try:
            async with SessionLocal() as session:
                now = datetime.now()

                # أولاً: فحص المنشورات التي حان وقت نشرها
                stmt_send = select(ScheduledPost).where(
                    ScheduledPost.post_date <= now,
                    ScheduledPost.is_sent == False
                )
                result_send = await session.execute(stmt_send)
                posts_to_send = result_send.scalars().all()

                for post in posts_to_send:
                    try:
                        # نسخ الرسالة من المستخدم إلى القناة
                        msg = await bot.copy_message(
                            chat_id=post.channel_id,
                            from_chat_id=post.owner_id,
                            message_id=post.message_id
                        )
                        # حفظ آيدي الرسالة المرسلة لاستخدامها في الحذف لاحقاً
                        post.sent_message_id = msg.message_id
                        post.is_sent = True
                        await session.commit()
                        logging.info(f"✅ تم نشر المنشور {post.id} في القناة {post.channel_id}")
                    except Exception as e:
                        logging.error(f"❌ خطأ أثناء النشر المجدول للمنشور {post.id}: {e}")

                # ثانياً: فحص المنشورات التي حان وقت حذفها
                stmt_delete = select(ScheduledPost).where(
                    ScheduledPost.delete_date <= now,
                    ScheduledPost.is_sent == True,
                    ScheduledPost.is_deleted == False,
                    ScheduledPost.delete_date.is_not(None) # التأكد أن هناك تاريخ حذف أصلاً
                )
                result_delete = await session.execute(stmt_delete)
                posts_to_delete = result_delete.scalars().all()

                for post in posts_to_delete:
                    try:
                        # حذف الرسالة من القناة
                        await bot.delete_message(
                            chat_id=post.channel_id,
                            message_id=post.sent_message_id
                        )
                        post.is_deleted = True
                        await session.commit()
                        logging.info(f"🗑 تم حذف المنشور {post.id} تلقائياً من القناة {post.channel_id}")
                    except Exception as e:
                        logging.error(f"❌ خطأ أثناء الحذف التلقائي للمنشور {post.id}: {e}")

        except Exception as e:
            logging.error(f"❌ خطأ في دورة المجدول: {e}")

        # الانتظار لمدة 60 ثانية قبل الفحص التالي
        await asyncio.sleep(60)
    
