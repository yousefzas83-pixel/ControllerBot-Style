from datetime import datetime
from sqlalchemy import BigInteger, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

# 1. جدول المستخدمين
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    plan: Mapped[str] = mapped_column(String(20), default="Free")
    sub_expire: Mapped[datetime] = mapped_column(DateTime, nullable=True)

# 2. جدول القنوات المربوطة
class Channel(Base):
    __tablename__ = "channels"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(BigInteger) # آيدي المستخدم صاحب القناة
    channel_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(255))

# 3. جدول المنشورات المجدولة والحذف التلقائي
class ScheduledPost(Base):
    __tablename__ = "scheduled_posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(BigInteger)
    channel_id: Mapped[int] = mapped_column(BigInteger)
    
    # بيانات الرسالة للنشر
    message_id: Mapped[int] = mapped_column(BigInteger) # آيدي الرسالة الأصلية لنسخها
    sent_message_id: Mapped[int] = mapped_column(BigInteger, nullable=True) # آيدي الرسالة بعد نشرها (للحذف)
    
    # المواعيد والحالات
    post_date: Mapped[datetime] = mapped_column(DateTime) # وقت النشر
    delete_date: Mapped[datetime] = mapped_column(DateTime, nullable=True) # وقت الحذف (إن وجد)
    
    is_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    
