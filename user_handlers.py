from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from app.keyboards.builders import main_menu_kb, plans_kb, support_kb
from datetime import datetime

user_router = Router()

# --- 1. الأمر الأساسي /start ---
@user_router.message(CommandStart())
async def cmd_start(message: types.Message):
    welcome_text = (
        "مرحبًا بك في <b>Controller Bot Style</b> 🚀\n\n"
        "النظام الأقوى لإدارة قنواتك وجدولة منشوراتك.\n"
        "• إدارة سهلة ومباشرة.\n"
        "• جدولة وحذف تلقائي.\n"
        "• دعم فني 24/7.\n\n"
        "ابدأ الآن باختيار أحد الخيارات 👇"
    )
    await message.answer(welcome_text, reply_markup=main_menu_kb(), parse_mode="HTML")

# --- 2. منطق الأزرار الرئيسية ---

# ➕ ربط قناة
@user_router.message(F.text == "➕ ربط قناة")
async def add_channel(message: types.Message):
    text = (
        "<b>خطوات ربط القناة:</b>\n\n"
        "1️⃣ قم بإضافة البوت @TBS1bot مشرفاً في قناتك.\n"
        "2️⃣ تأكد من إعطائه صلاحية 'نشر الرسائل'.\n"
        "3️⃣ قم بتوجيه (Forward) رسالة من القناة إلى هنا.\n\n"
        "⚠️ سيتم التحقق من الصلاحيات وحفظ القناة تلقائياً."
    )
    await message.answer(text, parse_mode="HTML")

# 📊 خطتي الحالية
@user_router.message(F.text == "📊 خطتي الحالية")
async def my_plan(message: types.Message):
    # ملاحظة: سيتم جلب هذه البيانات لاحقاً من قاعدة البيانات
    text = (
        "<b>📋 تفاصيل اشتراكك الحالي:</b>\n\n"
        "• الخطة: <b>Free</b>\n"
        "• القنوات المسموحة: 1\n"
        "• تاريخ الانتهاء: لا ينتهي\n"
        "• الحالة: نشط ✅"
    )
    await message.answer(text, parse_mode="HTML")

# ⬆️ ترقية الاشتراك
@user_router.message(F.text == "⬆️ ترقية الاشتراك")
async def upgrade_plan(message: types.Message):
    await message.answer("اختر الباقة التي تناسب احتياجاتك 💎:", reply_markup=plans_kb())

# 💳 الدفع والاشتراك
@user_router.message(F.text == "💳 الدفع والاشتراك")
async def payment_info(message: types.Message):
    text = (
        "<b>💳 معلومات الدفع المتاحة:</b>\n\n"
        "• <b>USDT (TRC20):</b>\n"
        "<code>TXXXXXXXXXXXXXXXXXXXXXXXXX</code>\n\n"
        "• <b>PayPal:</b>\n"
        "<code>your-email@example.com</code>\n\n"
        "⚠️ بعد التحويل، يرجى إرسال صورة الإيصال للدعم الفني للتفعيل."
    )
    await message.answer(text, parse_mode="HTML")

# 🛠 الدعم الفني
@user_router.message(F.text == "🛠 الدعم الفني")
async def support(message: types.Message):
    await message.answer("يمكنك التواصل مع المطور أو الانضمام لقناة التحديثات:", reply_markup=support_kb())

# 📖 شرح الاستخدام
@user_router.message(F.text == "📖 شرح الاستخدام")
async def help_guide(message: types.Message):
    guide = (
        "<b>📖 دليل الاستخدام السريع:</b>\n\n"
        "1. استخدم زر ➕ لربط قناتك.\n"
        "2. استخدم زر 📝 لجدولة أول منشور لك.\n"
        "3. اتبع تعليمات البوت لتحديد وقت النشر والحذف.\n\n"
        "للمزيد من المساعدة تواصل مع الدعم."
    )
    await message.answer(guide, parse_mode="HTML")

# --- 3. لوحة الأدمن (مخصصة لك فقط) ---
@user_router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id == 8511180085:
        from app.keyboards.builders import admin_panel_kb
        await message.answer("🛠 مرحباً بك يا مطور <b>Y ⁹|⁴ S</b> في لوحة الإدارة:", 
                           reply_markup=admin_panel_kb(), parse_mode="HTML")
    else:
        await message.answer("❌ هذا الأمر مخصص للإدارة فقط.")
