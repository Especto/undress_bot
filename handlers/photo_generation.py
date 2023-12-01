import asyncio

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from handlers import SystemVariables
from handlers.additionaly import get_user
from keyboards.inline.keyboards import __ as _i
from keyboards.inline.keyboards import *
from states.chat_states import ChatStates
from keyboards.localization import _
from utils.db.generations import add_generation
from utils.undress.api import upload_image_and_get_task_id, start_generation, check_status
from utils.db.users import update_gens

ACTIVE = SystemVariables.ACTIVE


async def get_upload(call: CallbackQuery, state: FSMContext):
    user = await get_user(state, call.message.chat.id)
    if user.gen_avail + user.gen_trial > 0:
        await call.message.edit_text(_("wait_photo", user.lang))
        await state.set_state(ChatStates.GetPhoto)
    else:
        await call.message.edit_text(_("run_out", user.lang), reply_markup=_i(buy_buttons, user.lang, [1, 1]))


async def get_photo(message: Message, bot, state: FSMContext):
    user = await get_user(state, message.from_user.id)
    file = await bot.get_file(message.photo[-1].file_id)
    input_path = f'photos/{message.from_user.id}_{file.file_id[-10:]}.jpg'
    await bot.download_file(file.file_path, input_path)
    await state.update_data(input_path=input_path)
    await bot.send_message(chat_id=user.user_id, text=_("select_mode", user.lang), reply_markup=_i(generation_mode, user.lang, [1,2]))


async def get_mode(call: CallbackQuery, state: FSMContext):
    user = await get_user(state, call.message.from_user.id)
    mode = call.data.split("_")[1].upper()
    await state.update_data(mode=mode)
    await call.message.edit_text(text=_("select_body_type", user.lang), reply_markup=_i(body_type, user.lang, [1, 3, 3]))


async def get_body_type(call: CallbackQuery, state: FSMContext, bot):
    user = await get_user(state, call.message.from_user.id)
    body_type = call.data.split("_")[1].upper()
    await state.update_data(body_type=body_type)
    text = _("generate_photo", user.user_id).replace('??', '..', 1).replace('?', '∞%', 1).replace('?', '∞', 1)
    message = await call.message.edit_text(text=text)
    await generate_photo(message, bot, state)


async def generate_photo(message, bot, state: FSMContext):
    try:
        global ACTIVE
        ACTIVE += 1
        data = await state.get_data()
        user = data.get('user')
        task_id = await upload_image_and_get_task_id(data.get('input_path'))
        await start_generation(task_id, data.get('mode'), data.get('body_type'))
        status = await check_status(task_id)
        i = 0
        while status["status"] != 'COMPLETED':
            i += 1
            text = _("generate_photo", user.user_id).replace('??', '.' * (i % 3), 1).replace('?', str(
                status['progress']) + '%', 1).replace('?', str(status['queuePosition']), 1)
            await message.edit_text(text=text)
            await asyncio.sleep(0.5)
            status = await check_status(task_id)
        add_generation(user.user_id, status, data.get('mode'), data.get('body_type'))
        await message.edit_text(_("generation_done", user.lang))

        await bot.send_photo(user.user_id, photo=status["resultUrl"])
        if user.gen_avail > 0:
            update_gens(user.user_id, "gen_avail", -1)
        else:
            update_gens(user.user_id, "gen_trial", -1)

        update_gens(user.user_id, "gen_done", 1)
        await state.clear()
        await bot.send_message(user.user_id, _("one_more", user.lang), reply_markup=_i(menu_buttons, user.lang, [2, 2, 2]))
        ACTIVE -= 1
    except:
        print(user.user_id, status, data.get('mode'), data.get('body_type'))



