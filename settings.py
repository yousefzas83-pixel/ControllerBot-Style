import os

# جلب المتغيرات مباشرة من النظام لضمان عدم ضياعها
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

# جلب وتصحيح رابط قاعدة البيانات
raw_db_url = os.getenv("DATABASE_URL", "")

if raw_db_url.startswith("postgres://"):
    DATABASE_URL = raw_db_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif raw_db_url.startswith("postgresql://"):
    DATABASE_URL = raw_db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
else:
    DATABASE_URL = raw_db_url

# كلاس بسيط لتنظيم البيانات كما يحب الكود الخاص بك
class Settings:
    def __init__(self):
        self.bot_token = BOT_TOKEN
        self.admin_id = ADMIN_ID
        self.db_url = DATABASE_URL

config = Settings()
