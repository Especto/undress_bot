from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from handlers.additionaly import get_user
from keyboards.reply.keyboards import __ as _r
from keyboards.reply.keyboards import *
from keyboards.inline.keyboards import __ as _i
from keyboards.inline.keyboards import *
from keyboards.localization import _
from utils.db.users import add_user, update_ref, update_lang


async def get_start(message: Message, state: FSMContext):
    user = await get_user(state, message.from_user.id)
    if user:
        await state.update_data(user=user)
        await message.answer(_("welcome_message", user.lang), reply_markup=_r(menu_keyboard, user.lang))
    else:
        ref_code = None
        if " " in message.text:
            ref_code = message.text.split()[1]
            try:
                ref_code = int(ref_code)
            except ValueError:
                pass
        await state.update_data(ref_code=ref_code)
        await state.update_data(user=message.from_user)
        await message.answer(_("agreement", message.from_user.language_code), reply_markup=_i(privacy_policy_buttons, message.from_user.language_code))


async def get_pp(call: CallbackQuery, state: FSMContext, bot):
    await call.message.delete()
    data = await state.get_data()
    user = add_user(data.get('user'), data.get('ref_code'))
    if data.get('ref_code') is not None:
        update_ref(data.get('ref_code'))
    await state.update_data(user=user)
    await bot.send_message(user.user_id, _("welcome_message", user.lang), reply_markup=_r(menu_keyboard, user.lang, [1]))


async def get_menu_callback(call: CallbackQuery, state: FSMContext):
    await get_menu(call.message, state)


async def get_menu(message: Message, state: FSMContext):
    user = await get_user(state, message.chat.id)
    await message.answer(_("welcome_message", user.lang), reply_markup=_i(menu_buttons, user.lang, [2, 2, 2]))


async def get_account(call: CallbackQuery, state: FSMContext):
    user = await get_user(state, call.message.chat.id)
    text = _('account_info', user.lang)
    for i in [user.gen_avail + user.gen_trial, user.gen_done, user.reg_date, user.ref_code, user.refs, user.lang]:
        text = text.replace('?', str(i), 1)
    await call.message.edit_text(text, reply_markup=_i(account_buttons, user.lang, [2, 1]))


async def get_lang(call: CallbackQuery, state: FSMContext):
    user = await get_user(state, call.message.chat.id)
    keyboard = InlineKeyboardBuilder()
    for button in set_language_buttons:
        if button.text == "bn_back":
            button.text = _("bn_back", user.lang)
        keyboard.button(text=button.text, callback_data=button.callback_data)
    keyboard.adjust(3, 1)
    await call.message.edit_text(_("choose_lang", user.lang), reply_markup=keyboard.as_markup())


async def set_lang(call: CallbackQuery):
    lang = call.data.split('_')[2]
    update_lang(call.from_user.id, lang)
    await call.answer(_("lang_chosen", lang))


async def buy_gen(call: CallbackQuery, state: FSMContext):
    user = await get_user(state, call.message.chat.id)
    await call.message.edit_text(_("buy_gen", user.lang), reply_markup=_i(price_list_button, user.lang, [2, 2, 2, 1]))


async def get_coming_soon(call: CallbackQuery, state: FSMContext):
    #user = await get_user(state, call.message.chat.id)
    await call.answer("Cooming soon")
