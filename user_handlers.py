from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
# تصحيح المسار: استدعاء مباشرة من builders.py الموجود في المجلد الرئيسي
from builders import main_menu_kb, plans_kb, support_kb, admin_panel_kb
from datetime import datetime

user_router = Router()

# --- 1. الأمر الأساسي /start ---
@user_router.message(CommandStart())
async def cmd_start(message: types.Message):
    welcome_text = (
        "مرحبًا بك في <b>Controller Bot Style</b> 🚀\n\n"
        "النظام الأقوى لإدارة قنواتك وجدولة منشوراتك.\n"
        "ابدأ الآن باختيار أحد الخيارات 👇"
    )
    # تأكد أن دالة main_menu_kb موجودة في ملف builders.py
    await message.answer(welcome_text, reply_markup=main_menu_kb(), parse_mode="HTML")

# --- 2. منطق الأزرار الرئيسية ---

@user_router.message(F.text == "➕ ربط قناة")
async def add_channel(message: types.Message):
    text = "<b>خطوات ربط القناة:</b>\n\n1️⃣ أضف البوت مشرفاً.\n2️⃣ وجه رسالة من القناة هنا."
    await message.answer(text, parse_mode="HTML")

@user_router.message(F.text == "📊 خطتي الحالية")
async def my_plan(message: types.Message):
    text = "<b>📋 تفاصيل اشتراكك الحالي:</b>\n\n• الخطة: <b>Free</b>\n• الحالة: نشط ✅"
    await message.answer(text, parse_mode="HTML")

@user_router.message(F.text == "⬆️ ترقية الاشتراك")
async def upgrade_plan(message: types.Message):
    await message.answer("اختر الباقة المناسبة 💎:", reply_markup=plans_kb())

@user_router.message(F.text == "🛠 الدعم الفني")
async def support(message: types.Message):
    await message.answer("تواصل مع المطور:", reply_markup=support_kb())

# --- 3. لوحة الأدمن ---
@user_router.message(Command("admin"))
async def admin_panel(message: types.Message):
    # تم تصحيح الـ ID والمسار هنا
    if message.from_user.id == 8511180085:
        await message.answer("🛠 مرحباً بك في لوحة الإدارة:", 
                           reply_markup=admin_panel_kb(), parse_mode="HTML")
    else:
        await message.answer("❌ هذا الأمر مخصص للإدارة فقط.")
        
