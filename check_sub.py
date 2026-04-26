from aiogram import BaseMiddleware
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

class CheckSubscriptionMiddleware(BaseMiddleware):
    async def call(self, handler, event: Message, data):
        CHANNEL_ID = -1003984865609  # ID قناتك
        try:
            member = await event.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=event.from_user.id)
            if member.status in ["left", "kicked"]: raise Exception()
        except:
            kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📢 اشترك في القناة", url="https://t.me")]])
            return await event.answer("⚠️ يجب الاشتراك في القناة أولاً لاستخدام البوت!", reply_markup=kb)
        return await handler(event, data)
