from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from keyboards.localization import _


menu_keyboard = (
        KeyboardButton(text="bn_menu"),
)


def __(buttons, locale, adjust=[]):
    try:
        keyboard = ReplyKeyboardBuilder()
        for button in buttons:
            text = _(button.text, locale)
            keyboard.button(text=text)
        keyboard.adjust(*adjust)
        return keyboard.as_markup()
    except Exception as e:
        print(e)

