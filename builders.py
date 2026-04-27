import os
# ... الاستيرادات السابقة تبقى كما هي ...

# جلب الرابط بأمان
db_url = os.getenv("DATABASE_URL", "")

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(url=db_url)
AsyncSessionLocal = async_sessionmaker(engine)

# ... بقية دوال الأزرار والمجدول تبقى كما هي ...
