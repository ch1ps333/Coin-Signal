from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from translate import translate as ts
from datebase.user import get_lang

async def display_coin_spot(link, tg_id, name_coin):
    button_link = InlineKeyboardButton(text=ts("Перейти до торгівлі", await get_lang(tg_id)), url=link)
    button_add_fav_coin = InlineKeyboardButton(text=ts('Додати до обраних', await get_lang(tg_id)), callback_data=f'add_fav_{name_coin}')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            button_link,
            button_add_fav_coin
        ]
    ])
    return keyboard


