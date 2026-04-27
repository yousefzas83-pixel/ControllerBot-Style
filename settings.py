import os
from dataclasses import dataclass

@dataclass
class Settings:
    bot_token: str
    admin_id: int
    db_url: str
    redis_url: str

def load_settings():
    # استخدام os.getenv مباشرة لجلب البيانات من إعدادات Railway
    return Settings(
        bot_token=os.getenv("BOT_TOKEN", "MISSING"),
        admin_id=int(os.getenv("ADMIN_ID", 0)),
        db_url=os.getenv("DATABASE_URL", "sqlite:///db.sqlite3"),
        redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0")
    )

config = load_settings()
