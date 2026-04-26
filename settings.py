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
        bot_token=env.str("BOT_TOKEN"),
        admin_id=env.int("ADMIN_ID"),
        db_url=env.str("DATABASE_URL"),
        redis_url=env.str("REDIS_URL")
    )

config = load_settings()
