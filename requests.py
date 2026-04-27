import os
from models import User, Channel, Base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, update, delete
from datetime import datetime

# جلب الرابط مباشرة من النظام هنا لضمان وجوده
db_url = os.getenv("DATABASE_URL", "")

# تصحيح الرابط يدوياً داخل الملف لقطع الشك باليقين
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# إذا كان الرابط لا يزال فارغاً (لحمايته من الانهيار)
if not db_url:
    print("Error: DATABASE_URL is not set!")
    # يمكنك وضع رابط افتراضي هنا للتجربة فقط إذا أردت
    db_url = "postgresql+asyncpg://postgres:password@localhost:5432/postgres"

# إعداد المحرك
engine = create_async_engine(url=db_url, echo=True)
async_session = async_sessionmaker(engine)

async def db_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# --- باقي العمليات (set_user, get_user_data, etc.) تبقى كما هي ---
# انسخ باقي الدوال من ملفك القديم هنا
