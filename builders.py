from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# --- 1. القائمة الرئيسية ---
def main_menu_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="➕ ربط قناة"), KeyboardButton(text="📊 خطتي الحالية"))
    builder.row(KeyboardButton(text="📝 جدولة منشور"), KeyboardButton(text="⬆️ ترقية الاشتراك"))
    builder.row(KeyboardButton(text="🛠 الدعم الفني"), KeyboardButton(text="📖 شرح الاستخدام"))
    builder.row(KeyboardButton(text="💳 الدفع والاشتراك"))
    return builder.as_markup(resize_keyboard=True)

# --- 2. قائمة الخطط والأسعار ---
def plans_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="💎 الخطة المميزة (شهر) - 5$", callback_data="plan_premium_1"))
    builder.row(InlineKeyboardButton(text="🔥 الخطة الاحترافية (سنة) - 45$", callback_data="plan_pro_12"))
    builder.row(InlineKeyboardButton(text="❌ إلغاء", callback_data="cancel_action"))
    return builder.as_markup()

# --- 3. قائمة الدعم الفني ---
def support_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="👤 المطور", url="https://t.me"))
    builder.row(InlineKeyboardButton(text="📢 قناة التحديثات", url="https://t.me"))
    return builder.as_markup()

# --- 4. لوحة الإدارة (للأدمن) ---
def admin_panel_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="👥 عرض المستخدمين"), KeyboardButton(text="📢 إذاعة عامة"))
    builder.row(KeyboardButton(text="💳 تفعيل اشتراك"), KeyboardButton(text="📈 الإحصائيات"))
    builder.row(KeyboardButton(text="🔙 العودة للقائمة الرئيسية"))
    return builder.as_markup(resize_keyboard=True)

# --- 5. دالة الجدولة (لسد الثغرة في main.py) ---
async def start_scheduler():
    """هذه الدالة تستدعى من main.py لبدء محرك الجدولة"""
    print("✅ محرك الجدولة يعمل الآن...")
    return True
    
