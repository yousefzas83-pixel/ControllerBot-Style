import os
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models import Base, User, Channel, ScheduledPost

# 1. جلب وتصحيح رابط قاعدة البيانات ليدعم الاتصال غير المتزامن (Async)
db_url = os.getenv("DATABASE_URL", "")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif db_url.startswith("postgresql://"):
    if "+asyncpg" not in db_url:
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# 2. إنشاء محرك قاعدة البيانات وجلسات الاتصال
engine = create_async_engine(url=db_url, echo=False)
async_session = async_sessionmaker(engine)

async def db_main():
    """إنشاء الجداول في قاعدة البيانات إذا لم تكن موجودة"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# --- عمليات المستخدمين ---

async def set_user(tg_id: int, username: str = None):
    """تسجيل مستخدم جديد أو تحديث بياناته"""
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == tg_id))
        if not user:
            session.add(User(telegram_id=tg_id, username=username))
            await session.commit()

async def get_user_data(tg_id: int):
    """جلب بيانات المستخدم بالكامل"""
    async with async_session() as session:
        return await session.scalar(select(User).where(User.telegram_id == tg_id))

# --- عمليات القنوات ---

async def add_channel(owner_id: int, channel_id: int, name: str):
    """إضافة قناة جديدة لقاعدة البيانات"""
    async with async_session() as session:
        channel = await session.scalar(select(Channel).where(Channel.channel_id == channel_id))
        if not channel:
            session.add(Channel(owner_id=owner_id, channel_id=channel_id, name=name))
            await session.commit()
            return True
        return False

async def get_my_channels(owner_id: int):
    """جلب قائمة القنوات المربوطة بمستخدم معين"""
    async with async_session() as session:
        result = await session.scalars(select(Channel).where(Channel.owner_id == owner_id))
        return result.all()

# --- عمليات المنشورات المجدولة ---

async def add_scheduled_post(owner_id, channel_id, post_date, message_id, delete_date=None):
    """حفظ منشور جديد في جدول الجدولة مع خيار الحذف التلقائي"""
    async with async_session() as session:
        new_post = ScheduledPost(
            owner_id=owner_id,
            channel_id=channel_id,
            post_date=post_date,
            message_id=message_id,
            delete_date=delete_date,
            is_sent=False,
            is_deleted=False
        )
        session.add(new_post)
        await session.commit()
        return True

async def get_pending_posts():
    """جلب المنشورات التي تنتظر النشر (يستخدمها المجدول)"""
    async with async_session() as session:
        result = await session.scalars(
            select(ScheduledPost).where(ScheduledPost.is_sent == False)
        )
        return result.all()

async def get_deletable_posts():
    """جلب المنشورات التي تنتظر الحذف التلقائي (يستخدمها المجدول)"""
    async with async_session() as session:
        result = await session.scalars(
            select(ScheduledPost).where(
                ScheduledPost.is_sent == True,
                ScheduledPost.is_deleted == False,
                ScheduledPost.delete_date != None
            )
        )
        return result.all()
                                                       
