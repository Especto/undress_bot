from aiogram.types import Message

from handlers import SystemVariables

from utils.db.generations import count_generations_today
from utils.db.users import get_user_db, count_users_today
from keyboards.localization import _

BLACK_LIST = SystemVariables.BLACK_LIST
ACTIVE = SystemVariables.ACTIVE
BREAK = SystemVariables.BREAK


async def block_account(message: Message):
    try:
        user_id = int(message.text.split()[1])
        BLACK_LIST.append(user_id)
        await message.answer(f"{user_id} заблокирован.")
    except:
        await message.answer(f"user_id не получен.")


async def unlock_account(message: Message):
    try:
        user_id = int(message.text.split()[1])
        if user_id in BLACK_LIST:
            BLACK_LIST.remove(user_id)
            await message.answer(f"{user_id} разблокирован.")
        else:
            await message.answer(f"{user_id} такого пользователя нет.")
    except:
        await message.answer(f"user_id не получен.")


async def check_account(message: Message):
    try:
        user_id = int(message.text.split()[1])
        user = get_user_db(int(user_id))
        text = _('account_info', "ru")
        for i in [user.gen_avail + user.gen_trial, user.gen_done, user.reg_date, user.ref_code, user.refs, user.lang]:
            text = text.replace('?', str(i), 1)
        await message.answer(text)
    except:
        await message.answer(f"user_id не получен.")


async def check_stat(message: Message):
    gens = count_generations_today()
    users = count_users_today()
    await message.answer(f"Пользователей: {users}\nГенераций: {gens}\nСейчас генерируется: {ACTIVE}")


async def get_break(message: Message):
    global BREAK
    BREAK = not BREAK
    await message.answer(f"Break is {BREAK}")

