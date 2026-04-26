from app.database.models import User, Channel, Base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, update, delete
from app.config.settings import config
from datetime import datetime

# إعداد محرك قاعدة البيانات والاتصال
engine = create_async_engine(url=config.db_url, echo=True)
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
            return True
        return False

async def get_user_data(tg_id: int):
    """جلب بيانات المستخدم بالكامل (الخطة، تاريخ الانتهاء)"""
    async with async_session() as session:
        return await session.scalar(select(User).where(User.telegram_id == tg_id))

# --- عمليات القنوات ---

async def add_channel(owner_id: int, channel_id: int, name: str):
    """إضافة قناة جديدة لقاعدة البيانات"""
    async with async_session() as session:
        # التحقق إذا كانت القناة مضافة مسبقاً
        channel = await session.scalar(select(Channel).where(Channel.channel_id == channel_id))
        
        if not channel:
            session.add(Channel(owner_id=owner_id, channel_id=channel_id, name=name))
            await session.commit()
            return True
        return False

async def get_my_channels(owner_id: int):
    """جلب كافة القنوات التابعة لمستخدم معين"""
    async with async_session() as session:
        result = await session.scalars(select(Channel).where(Channel.owner_id == owner_id))
        return result.all()

# --- عمليات الاشتراكات (للأدمن) ---

async def update_subscription(tg_id: int, plan_name: str, expire_date: datetime):
    """تحديث خطة المستخدم وتاريخ انتهائها"""
    async with async_session() as session:
        await session.execute(
            update(User).where(User.telegram_id == tg_id)
            .values(plan=plan_name, sub_expire=expire_date)
        )
        await session.commit()
