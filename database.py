from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import config

# استخدام الرابط المعالج من ملف الإعدادات
engine = create_engine(config.db_url)

# إنشاء جلسة الاتصال (Session)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
