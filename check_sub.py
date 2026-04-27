from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message

class CheckSubscriptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # هنا يمكنك إضافة منطق التحقق من الاشتراك لاحقاً
        # حالياً سنجعله يمرر الرسالة فقط لكي يعمل البوت
        return await handler(event, data)
        
