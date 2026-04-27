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
    
