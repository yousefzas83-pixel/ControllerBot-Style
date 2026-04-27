import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# استيراد ملفات المشروع (تأكد أن هذه الملفات موجودة في GitHub)
from requests import db_main
from user_handlers import user_router
from builders import start_scheduler 

# --- جلب التوكن بأمان من متغيرات البيئة (الأمان أولاً 🛡️) ---
BOT_TOKEN = os.getenv("BOT_TOKEN")

# إعداد السجلات لمراقبة أداء البوت في Railway
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

async def main():
    # التحقق من وجود التوكن لضمان عدم انهيار التطبيق
    if not BOT_TOKEN:
        logging.error("❌ خطأ حرج: BOT_TOKEN غير موجود في متغيرات Railway!")
        return

    # إنشاء كائن البوت
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # إنشاء الموزع وتوصيل الرواتر (Handlers)
    dp = Dispatcher()
    dp.include_router(user_router)

    print("🚀 جاري تهيئة قاعدة البيانات والمجدول...")
    try:
        # تشغيل تهيئة قاعدة البيانات
        await db_main()
        # تشغيل محرك الجدولة (النشر والحذف التلقائي) في الخلفية
        asyncio.create_task(start_scheduler(bot))
        print("✅ القاعدة والمجدول في حالة جاهزية.")
    except Exception as e:
        logging.warning(f"⚠️ تنبيه في بدء التشغيل: {e}")

    try:
        # حذف التحديثات المعلقة لضمان استجابة سريعة فور التشغيل
        await bot.delete_webhook(drop_pending_updates=True)
        print("✨ البوت يعمل الآن بنجاح ويستقبل الأوامر!")
        
        # بدء استقبال الرسائل
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"❌ خطأ غير متوقع أثناء تشغيل البوت: {e}")
    finally:
        # إغلاق الجلسة عند التوقف
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("🛑 تم إيقاف البوت يدوياً.")
        
