from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from translate import translate as ts
from datebase.user import get_lang

async def display_coin_spot(link, tg_id):
    button_link = InlineKeyboardButton(text=ts("Перейти до торгівлі", await get_lang(tg_id)), url=link)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [button_link]
    ])
    return keyboard
