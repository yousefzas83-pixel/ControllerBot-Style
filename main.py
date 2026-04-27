import asyncio
import logging
import sys

# استيراد المكونات الأساسية للبوت (ضروري جداً)
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# استيراد الملفات مباشرة لأنها موجودة في المجلد الرئيسي (بدون كلمة app أو config)
import settings
from requests import db_main
from user_handlers import user_router
from check_sub import CheckSubscriptionMiddleware
from builders import start_scheduler 

# تعريف متغير الإعدادات لاستخدامه في البوت
config = settings.config

# إعداد السجلات (Logs) لمراقبة عمل البوت في Railway
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

async def on_startup():
    """وظائف يتم تنفيذها عند تشغيل البوت"""
    print("--- 🚀 جاري بدء تشغيل البوت ---")
    
    # 1. إنشاء جداول قاعدة البيانات إذا لم تكن موجودة
    await db_main()
    print("✅ قاعدة البيانات جاهزة.")

    # 2. تشغيل محرك الجدولة (النشر التلقائي)
    await start_scheduler()
    print("✅ محرك الجدولة يعمل الآن.")

async def main():
    # إنشاء كائن البوت مع دعم HTML
    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # إنشاء الموزع (Dispatcher)
    dp = Dispatcher()

    # --- تسجيل الميدل وير (الاشتراك الإجباري) ---
    dp.message.middleware(CheckSubscriptionMiddleware())

    # --- تسجيل الرواتر (Handlers) ---
    dp.include_router(user_router)

    # تنفيذ وظائف بدء التشغيل
    await on_startup()

    try:
        print("✨ البوت يعمل الآن بنجاح!")
        # حذف التحديثات القديمة وبدء الاستقبال
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"❌ حدث خطأ غير متوقع: {e}")
    finally:
        await bot.session.close()

# تصحيح شرط التشغيل الأساسي
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("--- 🛑 تم إيقاف البوت ---")
    
