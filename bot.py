from aiogram import Bot, F, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart, and_f
from aiogram.filters.command import Command
import re

from handlers.admin import block_account, unlock_account, check_account, check_stat, get_break
from handlers.client_menu import *
from handlers.photo_generation import get_photo, get_upload, get_mode, get_body_type
from states.chat_states import ChatStates
from utils.config import config

ADMIN_ID = config.tg.admin_id

bot = Bot(token=config.tg.token, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())

dp.message.register(get_start, CommandStart())
dp.message.register(get_menu, ((F.text == "Menu") | (F.text == "Меню")))
dp.callback_query.register(get_menu_callback, F.data == "back_menu")
dp.callback_query.register(get_pp, F.data == "agree_policy")
dp.callback_query.register(get_account, ((F.data == 'account') | (F.data == "back_account")))
dp.callback_query.register(get_coming_soon, F.data == "faq")
dp.callback_query.register(get_coming_soon, F.data == "promo")
dp.callback_query.register(get_coming_soon, F.data == "partner")
dp.callback_query.register(get_lang, (F.data == "change_lang"))
dp.callback_query.register(set_lang, F.data.startswith('set_language_'))
dp.callback_query.register(buy_gen, F.data == "buy_gen")

dp.callback_query.register(get_upload, F.data == "upload_photo")
dp.message.register(get_photo, and_f(ChatStates.GetPhoto, F.photo))
dp.callback_query.register(get_mode, F.data.startswith('mode_'))
dp.callback_query.register(get_body_type, F.data.startswith('body_'))

dp.message.register(block_account, and_f(Command(re.compile(r"^block")), F.from_user.id.in_({ADMIN_ID})))
dp.message.register(unlock_account, and_f(Command(re.compile(r"^unblock")), F.from_user.id.in_({ADMIN_ID})))
dp.message.register(check_account, and_f(Command(re.compile(r"^check_account")), F.from_user.id.in_({ADMIN_ID})))
dp.message.register(check_stat, and_f(Command("check_stat"), F.from_user.id.in_({ADMIN_ID})))
dp.message.register(get_break, and_f(Command("set_break"), F.from_user.id.in_({ADMIN_ID})))

