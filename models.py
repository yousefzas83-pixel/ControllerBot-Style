from datetime import datetime
from sqlalchemy import BigInteger, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    plan: Mapped[str] = mapped_column(String(20), default="Free")
    sub_expire: Mapped[datetime] = mapped_column(DateTime, nullable=True)

class Channel(Base):
    __tablename__ = "channels"
    id: Mapped[int] = mapped_column(primary_key=True)
    # التعديل هنا: الربط يجب أن يكون بـ users.id وليس telegram_id لضمان استقرار القاعدة
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    channel_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(255))
    
