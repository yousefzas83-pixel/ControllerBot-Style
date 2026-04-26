from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# 1. لوحة المستخدم الرئيسية (Reply Keyboard)
def main_menu_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    
    # توزيع الأزرار حسب المرحلة 10
    builder.button(text="➕ ربط قناة")
    builder.button(text="📂 إدارة قنواتي")
    builder.button(text="📝 جدولة منشور")
    builder.button(text="📊 خطتي الحالية")
    builder.button(text="⬆️ ترقية الاشتراك")
    builder.button(text="💳 الدفع والاشتراك")
    builder.button(text="⚙️ الإعدادات")
    builder.button(text="🛠 الدعم الفني")
    builder.button(text="📖 شرح الاستخدام")
    
    # تنظيم الصفوف: 2 أزرار في كل صف، والشرح في صف منفرد
    builder.adjust(2, 2, 2, 2, 1)
    return builder.as_markup(resize_keyboard=True, input_field_placeholder="اختر من القائمة...")

# 2. لوحة الأدمن (Inline Keyboard)
def admin_panel_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text="👥 المستخدمين", callback_data="admin_users")
    builder.button(text="💰 المدفوعات", callback_data="admin_payments")
    builder.button(text="📦 الاشتراكات", callback_data="admin_subs")
    builder.button(text="📊 الإحصائيات", callback_data="admin_stats")
    builder.button(text="🚫 الحظر", callback_data="admin_ban")
    builder.button(text="📢 رسالة جماعية", callback_data="admin_broadcast")
    
    builder.adjust(2)
    return builder.as_markup()

# 3. أزرار اختيار الخطط (Plans)
def plans_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text="🥉 Free (محدود)", callback_data="plan_free")
    builder.button(text="🥈 Pro (5$)", callback_data="plan_pro")
    builder.button(text="🥇 Business (10$)", callback_data="plan_business")
    builder.button(text="💎 VIP (Custom)", callback_data="plan_vip")
    
    builder.adjust(2)
    return builder.as_markup()

# 4. أزرار تأكيد الدفع (للأدمن)
def approve_payment_kb(user_id: int, plan: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text="✅ قبول وتفعيل", callback_data=f"pay_approve_{user_id}_{plan}")
    builder.button(text="❌ رفض الطلب", callback_data=f"pay_decline_{user_id}")
    
    builder.adjust(1)
    return builder.as_markup()

# 5. أزرار الدعم الفني والقناة
def support_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="👨‍💻 المطور", url="https://t.me")
    builder.button(text="📢 القناة الرسمية", url="https://t.me")
    return builder.as_markup()
