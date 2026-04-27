import asyncio
import logging
import sys

# استيراد المكونات الأساسية للبوت من aiogram 3.x
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# استيراد ملفات مشروعك (تأكد أن الأسماء مطابقة لملفاتك في GitHub)
import settings
from requests import db_main
from user_handlers import user_router
from check_sub import CheckSubscriptionMiddleware
from builders import start_scheduler 

# جلب الإعدادات من ملف settings.py
config = settings.config

# إعداد السجلات (Logs) لمراقبة عمل البوت في Railway
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

async def on_startup():
    """وظائف يتم تنفيذها فور تشغيل البوت"""
    print("--- 🚀 جاري بدء تشغيل البوت ---")
    
    # 1. إنشاء جداول قاعدة البيانات
    try:
        await db_main()
        print("✅ قاعدة البيانات جاهزة.")
    except Exception as e:
        logging.error(f"❌ خطأ في قاعدة البيانات: {e}")

    # 2. تشغيل محرك الجدولة
    try:
        await start_scheduler()
        print("✅ محرك الجدولة يعمل الآن.")
    except Exception as e:
        logging.error(f"❌ خطأ في محرك الجدولة: {e}")

async def main():
    # إنشاء كائن البوت
    # ملاحظة: تأكد أنك وضعت BOT_TOKEN في Variables في Railway
    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # إنشاء الموزع (Dispatcher)
    dp = Dispatcher()

    # تسجيل الميدل وير (الاشتراك الإجباري)
    dp.message.middleware(CheckSubscriptionMiddleware())

    # تسجيل الرواتر (الأوامر والرسائل)
    dp.include_router(user_router)

    # تشغيل مهام بدء التشغيل
    await on_startup()

    try:
        print("✨ البوت يعمل الآن بنجاح وبدون أخطاء!")
        # حذف التحديثات المعلقة وبدء استقبال الرسائل الجديدة
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"❌ حدث خطأ غير متوقع أثناء التشغيل: {e}")
    finally:
        await bot.session.close()

# شرط تشغيل الملف الأساسي
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("--- 🛑 تم إيقاف البوت يدوياً ---")
        
