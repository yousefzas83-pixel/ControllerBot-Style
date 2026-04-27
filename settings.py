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
    return Settings(
        bot_token=env.str("BOT_TOKEN", default="MISSING"),
        admin_id=env.int("ADMIN_ID", default=0),
        db_url=env.str("DATABASE_URL", default="sqlite:///db.sqlite3"),
        redis_url=env.str("REDIS_URL", default="redis://localhost:6379/0")
    )

config = load_settings()
