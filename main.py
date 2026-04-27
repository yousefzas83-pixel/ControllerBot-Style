import asyncio
import logging
import sys

# استيراد الإعدادات والملفات التي أنشأناها
from config.settings import config
from database.requests import db_main
from handlers.user_handlers import user_router
from middlewares.check_sub import CheckSubscriptionMiddleware
from services.scheduler import start_scheduler

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
    # إنشاء كائن البوت مع دعم HTML كوضع افتراضي للنصوص
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
        print(f"✨ البوت يعمل الآن على اليوزر: @TBS1bot")
        # بدء استقبال الرسائل (Polling)
        # تم إضافة skip_updates لتجاهل الرسائل القديمة التي أرسلت والبوت مطفأ
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logging.error(f"❌ حدث خطأ غير متوقع: {e}")
    finally:
        await bot.session.close()

if name == "main":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("--- 🛑 تم إيقاف البوت ---")
