import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# استيراد الملفات
from requests import db_main
from user_handlers import user_router
from builders import start_scheduler 

# التوكن المباشر الخاص بك (تأكد من صحته 100%)
BOT_TOKEN = "7573887081:AAH8u8YI_T18l0z6O_EwN-N0_EwN-N0_EwN"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

async def main():
    # إنشاء البوت
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # إنشاء الموزع
    dp = Dispatcher()

    # تسجيل الراوتر الخاص بالأوامر
    dp.include_router(user_router)

    print("🚀 جاري تهيئة قاعدة البيانات والمجدول...")
    try:
        await db_main()
        asyncio.create_task(start_scheduler(bot))
    except Exception as e:
        print(f"⚠️ تنبيه: فشل تشغيل المجدول أو القاعدة، لكن البوت سيستمر: {e}")

    # بدء استقبال الرسائل
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        print("✨ البوت متصل الآن ويستقبل الأوامر!")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
            
