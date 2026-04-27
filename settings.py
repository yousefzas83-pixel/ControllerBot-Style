from environs import Env
from dataclasses import dataclass

@dataclass
class Settings:
    bot_token: str
    admin_id: int
    db_url: str
    redis_url: str

def load_settings():
    env = Env()
    env.read_env()
    
    # جلب الرابط وتصحيحه تلقائياً إذا كان يبدأ بـ postgres://
    raw_db_url = env.str("DATABASE_URL")
    if raw_db_url.startswith("postgres://"):
        raw_db_url = raw_db_url.replace("postgres://", "postgresql://", 1)
    
    return Settings(
        bot_token=env.str("BOT_TOKEN"),
        admin_id=env.int("ADMIN_ID"), # تأكد أن هذا المتغير موجود في Railway وقيمته أرقام فقط
        db_url=raw_db_url,
        redis_url=env.str("REDIS_URL", "redis://localhost") # أضفنا قيمة افتراضية لتجنب الانهيار
    )

config = load_settings()
