import os
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models import Base, User, Channel, ScheduledPost

# جلب الرابط بأمان من متغيرات بيئة Railway 🛡️
db_url = os.getenv("DATABASE_URL", "")

# تصحيح البادئة تلقائياً لضمان عمل نظام الـ Async بدون أخطاء
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# إنشاء المحرك وجلسات الاتصال
engine = create_async_engine(url=db_url, echo=False)
async_session = async_sessionmaker(engine)

async def db_main():
    """إنشاء الجداول في قاعدة البيانات تلقائياً عند التشغيل"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# --- عمليات المستخدمين ---
async def set_user(tg_id: int, username: str = None):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == tg_id))
        if not user:
            session.add(User(telegram_id=tg_id, username=username))
            await session.commit()

async def get_user_data(tg_id: int):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.telegram_id == tg_id))

# --- عمليات القنوات ---
async def add_channel(owner_id: int, channel_id: int, name: str):
    async with async_session() as session:
        channel = await session.scalar(select(Channel).where(Channel.channel_id == channel_id))
        if not channel:
            session.add(Channel(owner_id=owner_id, channel_id=channel_id, name=name))
            await session.commit()
            return True
        return False

async def get_my_channels(owner_id: int):
    async with async_session() as session:
        result = await session.scalars(select(Channel).where(Channel.owner_id == owner_id))
        return result.all()

# --- عمليات الجدولة والحذف ---
async def add_scheduled_post(owner_id, channel_id, post_date, message_id, delete_date=None):
    async with async_session() as session:
        new_post = ScheduledPost(
            owner_id=owner_id, channel_id=channel_id, post_date=post_date,
            message_id=message_id, delete_date=delete_date
        )
        session.add(new_post)
        await session.commit()
        return True
        
