import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models import Base, User, Channel, ScheduledPost

# سحب الرابط مباشرة والتأكد من وجوده
db_url = os.getenv("DATABASE_URL")

if not db_url:
    # هذا الرابط وهمي فقط لمنع الانهيار إذا لم يجد المتغير
    db_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
else:
    # تصحيح البادئة يدوياً
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# إنشاء المحرك
engine = create_async_engine(url=db_url, echo=False)
async_session = async_sessionmaker(engine)

async def db_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# (باقي الدوال set_user و add_channel تبقى كما هي في ملفك الأصلي)
