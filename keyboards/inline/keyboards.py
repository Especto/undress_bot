from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.localization import _

menu_buttons = (
        InlineKeyboardButton(text="bn_upload_photo", callback_data='upload_photo'),
        InlineKeyboardButton(text="bn_buy_gen", callback_data='buy_gen'),
        InlineKeyboardButton(text="bn_acc", callback_data='account'),
        InlineKeyboardButton(text="bn_faq", callback_data='faq'),
        InlineKeyboardButton(text="bn_promo", callback_data='promo'),
        InlineKeyboardButton(text="bn_partner", callback_data='partner'),
)
set_language_buttons = (
        InlineKeyboardButton(text="🇺🇸English", callback_data='set_language_en'),
        InlineKeyboardButton(text="🇺🇦Українська", callback_data='set_language_ua'),
        InlineKeyboardButton(text="🇷🇺Русский", callback_data='set_language_ru'),
        InlineKeyboardButton(text="bn_back", callback_data='back_account')
)

privacy_policy_buttons = (
    InlineKeyboardButton(text="bn_pp_agree", callback_data='agree_policy'),
    InlineKeyboardButton(text="bn_pp_disagree", callback_data='disagree_policy')
)

account_buttons = (
    InlineKeyboardButton(text="bn_buy_gen", callback_data='buy_gen'),
    InlineKeyboardButton(text="bn_change_lang", callback_data='change_lang'),
    InlineKeyboardButton(text="bn_back", callback_data='back_menu')

)

buy_buttons = (
    InlineKeyboardButton(text="bn_buy_gen", callback_data="buy_gen"),
    InlineKeyboardButton(text="bn_back", callback_data="back_account")
)

generation_mode = (
    InlineKeyboardButton(text="bn_undress_mode", callback_data="mode_undress"),
    InlineKeyboardButton(text="bn_lingerie_mode", callback_data="mode_lingerie"),
    InlineKeyboardButton(text="bn_bikini_mode", callback_data="mode_bikini")
)

body_type = (
    InlineKeyboardButton(text="bn_auto_body", callback_data="body_auto"),
    InlineKeyboardButton(text="bn_slim_body", callback_data="body_slim"),
    InlineKeyboardButton(text="bn_skinny_body", callback_data="body_skinny"),
    InlineKeyboardButton(text="bn_curvy_body", callback_data="body_curvy"),
    InlineKeyboardButton(text="bn_athletic_body", callback_data="body_athletic"),
    InlineKeyboardButton(text="bn_chubby_body", callback_data="body_chubby"),
    InlineKeyboardButton(text="bn_hourglass_body", callback_data="body_hourglass")
)


price_list_button = (
    InlineKeyboardButton(text="2", callback_data="buy_150"),
    InlineKeyboardButton(text="150", callback_data="buy_150"),
    InlineKeyboardButton(text="4", callback_data="buy_300"),
    InlineKeyboardButton(text="300(0%)", callback_data="buy_300"),
    InlineKeyboardButton(text="6", callback_data="buy_400"),
    InlineKeyboardButton(text="400(%)", callback_data="buy_400"),
    InlineKeyboardButton(text="bn_back", callback_data="back_account")
)


def __(buttons, locale, adjust=[]):
    try:
        keyboard = InlineKeyboardBuilder()
        for button in buttons:
            text = _(button.text, locale)
            callback = button.callback_data
            keyboard.button(text=text, callback_data=callback)
        keyboard.adjust(*adjust)
        return keyboard.as_markup()
    except Exception as e:
        print(e)

