from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime, timedelta

# استيراد الأزرار والعمليات
from builders import main_menu_kb, plans_kb, support_kb, admin_panel_kb
import requests as rq

user_router = Router()

# تعريف مراحل الجدولة (States)
class PostStates(StatesGroup):
    choosing_channel = State()
    waiting_for_content = State()
    waiting_for_time = State()
    waiting_for_delete_time = State()

# --- 1. رسالة الترحيب الرئيسية ---
@user_router.message(CommandStart())
async def cmd_start(message: types.Message):
    await rq.set_user(message.from_user.id, message.from_user.username)
    welcome_text = (
        "🚀 <b>مرحباً بك في Controller Bot Style</b>\n\n"
        "النظام الأقوى لإدارة قنواتك، جدولة منشوراتك، والتحكم الكامل بالنشر الاحترافي داخل تيليجرام 🔥\n\n"
        "من هنا يمكنك:\n"
        "📌 إدارة جميع قنواتك بسهولة\n"
        "📆 جدولة المنشورات بدقة عالية\n"
        "⚡ نشر تلقائي سريع وآمن\n"
        "🛠 متابعة الدعم الفني المباشر\n"
        "📢 استقبال آخر التحديثات والإضافات الجديدة\n\n"
        "تم تصميم هذا النظام ليمنحك تجربة احترافية كاملة بدون تعقيد، مع سرعة أداء عالية وتحكم متقدم يناسب أصحاب القنوات الكبيرة والمحترفين 👑\n\n"
        "ابدأ الآن باختيار أحد الخيارات بالأسفل 👇"
    )
    await message.answer(welcome_text, reply_markup=main_menu_kb(), parse_mode="HTML")

# --- 2. شرح الاستخدام ---
@user_router.message(F.text == "📖 شرح الاستخدام")
async def help_guide(message: types.Message):
    guide_text = (
        "📖 <b>شرح استخدام @TBS1bot 🤖</b>\n\n"
        "يرجى اتباع الخطوات التالية بالترتيب:\n\n"
        "① ➕ <b>ربط قناة</b>: أضف البوت مشرفاً في قناتك ثم وجه رسالة منها إلى هنا.\n"
        "② 📝 <b>جدولة منشور</b>: اختر القناة، أرسل المحتوى، وحدد وقت النشر والحذف.\n"
        "③ 📊 <b>خطتي الحالية</b>: لمتابعة حالة اشتراكك وقنواتك.\n"
        "④ 🛠 <b>الدعم الفني</b>: للتواصل المباشر مع المطور.\n"
    )
    await message.answer(guide_text, parse_mode="HTML")

# --- 3. نظام ربط القنوات (Forward) ---
@user_router.message(F.text == "➕ ربط قناة")
async def ask_for_forward(message: types.Message):
    await message.answer(
        "<b>خطوات ربط القناة:</b>\n\n"
        "1️⃣ أضف البوت مشرفاً في قناتك بصلاحية 'نشر الرسائل'.\n"
        "2️⃣ قم بـ <b>توجيه (Forward)</b> أي رسالة من القناة إلى هنا 👇",
        parse_mode="HTML"
    )

@user_router.message(F.forward_from_chat.type == "channel")
async def handle_forward(message: types.Message):
    chat = message.forward_from_chat
    success = await rq.add_channel(message.from_user.id, chat.id, chat.title)
    if success:
        await message.answer(f"✅ <b>تم ربط القناة بنجاح!</b>\n📌 القناة: <b>{chat.title}</b>", parse_mode="HTML")
    else:
        await message.answer("⚠️ هذه القناة مربوطة بالفعل بنظامنا.")

# --- 4. نظام جدولة المنشورات (FSM) ---
@user_router.message(F.text == "📝 جدولة منشور")
async def start_scheduling(message: types.Message, state: FSMContext):
    channels = await rq.get_my_channels(message.from_user.id)
    if not channels:
        return await message.answer("❌ ليس لديك قنوات مربوطة. قم بربط قناة أولاً.")
    
    kb = InlineKeyboardBuilder()
    for ch in channels:
        kb.button(text=ch.name, callback_data=f"sel_ch_{ch.channel_id}")
    kb.adjust(1)
    await message.answer("اختر القناة للنشر 👇", reply_markup=kb.as_markup())
    await state.set_state(PostStates.choosing_channel)

@user_router.callback_query(F.data.startswith("sel_ch_"))
async def channel_selected(callback: types.CallbackQuery, state: FSMContext):
    ch_id = int(callback.data.split("_")[2])
    await state.update_data(selected_channel=ch_id)
    await callback.message.answer("📥 الآن أرسل المنشور (نص، صورة، فيديو).")
    await state.set_state(PostStates.waiting_for_content)
    await callback.answer()

@user_router.message(PostStates.waiting_for_content)
async def get_content(message: types.Message, state: FSMContext):
    await state.update_data(msg_id=message.message_id)
    await message.answer("🕒 أرسل وقت النشر بتنسيق: <code>2026-05-01 14:30</code>", parse_mode="HTML")
    await state.set_state(PostStates.waiting_for_time)

@user_router.message(PostStates.waiting_for_time)
async def get_time(message: types.Message, state: FSMContext):
    try:
        post_time = datetime.strptime(message.text, "%Y-%m-%d %H:%M")
        await state.update_data(post_time=message.text)
        
        kb = InlineKeyboardBuilder()
        kb.button(text="ساعة", callback_data="del_1"), kb.button(text="3 ساعات", callback_data="del_3")
        kb.button(text="24 ساعة", callback_data="del_24"), kb.button(text="بدون حذف", callback_data="del_0")
        kb.adjust(2)
        await message.answer("⏱ هل تريد حذف المنشور تلقائياً بعد النشر؟", reply_markup=kb.as_markup())
        await state.set_state(PostStates.waiting_for_delete_time)
    except ValueError:
        await message.answer("❌ التنسيق خاطئ! مثال: <code>2026-05-01 14:30</code>")

@user_router.callback_query(F.data.startswith("del_"))
async def finalize_post(callback: types.CallbackQuery, state: FSMContext):
    hours = int(callback.data.split("_")[1])
    data = await state.get_data()
    post_date = datetime.strptime(data['post_time'], "%Y-%m-%d %H:%M")
    delete_date = post_date + timedelta(hours=hours) if hours > 0 else None

    await rq.add_scheduled_post(
        owner_id=callback.from_user.id,
        channel_id=data['selected_channel'],
        post_date=post_date,
        message_id=data['msg_id'],
        delete_date=delete_date
    )
    await callback.message.answer(f"✅ تم الجدولة بنجاح!")
    await state.clear()
    await callback.answer()

# --- 5. بقية الأزرار ---
@user_router.message(F.text == "🛠 الدعم الفني")
async def support_info(message: types.Message):
    await message.answer("تواصل مع الإدارة مباشرة:", reply_markup=support_kb())

@user_router.message(F.text == "📊 خطتي الحالية")
async def my_plan(message: types.Message):
    data = await rq.get_user_data(message.from_user.id)
    plan = data.plan if data else "Free"
    await message.answer(f"📋 <b>اشتراكك الحالي:</b>\n• الخطة: {plan}\n• الحالة: نشط ✅", parse_mode="HTML")

@user_router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id == 8511180085: # تأكد من أن الـ ID صحيح
        await message.answer("🛠 لوحة الإدارة:", reply_markup=admin_panel_kb())
    
