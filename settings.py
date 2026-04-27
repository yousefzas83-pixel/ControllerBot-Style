import os

class Settings:
    def __init__(self):
        # جلب التوكن من خانة BOT_TOKEN
        self.bot_token = os.getenv("BOT_TOKEN")
        
        # جلب الآيدي من خانة ADMIN_ID وتحويله لرقم
        admin_id_raw = os.getenv("ADMIN_ID", "0")
        self.admin_id = int(admin_id_raw) if admin_id_raw.isdigit() else 0
        
        # جلب الرابط من خانة DATABASE_URL
        self.db_url = os.getenv("DATABASE_URL")

# إنشاء كائن الإعدادات لاستخدامه في البوت
config = Settings()
