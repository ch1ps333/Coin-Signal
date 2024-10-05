from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from asyncio import sleep
import aiohttp
from aiohttp import ClientSession
from typing import Optional
from os import getenv
from typing import Optional
from aiohttp import ClientSession
from aiogram.types import InlineKeyboardMarkup, BotCommand
from translate import translate as ts
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')

from datebase.user import reg_user, get_all_users, get_lang, add_signal_history
from keyboards.inline import display_coin_spot
from keyboards.reply import display_general_menu

router = Router()

commands = [
    BotCommand(command="/menu", description="Open general menu")
]

@router.message(Command(commands=['menu']))
async def send_welcome(message: Message):
    try:
        await message.answer(ts("Ви успішно повернулись в головне меню.", await get_lang(message.from_user.id)), reply_markup=await display_general_menu(message.from_user.id))
    except Exception as err:
     print(err)

@router.message(CommandStart())
async def cmd_start(message: Message):
    try:
        result = await reg_user(message.from_user.id, message.from_user.first_name)
        if result:
            await message.answer(ts("Ви успішно зареєструвались, бот надає інформацію по монетам, які показують різький зріст або падіння в ціні. По замовчуванню сигнали приходить при зрості і падінні монети на 5% та -5%, ви можете налаштувати поріг сигналів.", await get_lang(message.from_user.id)), reply_markup=await display_general_menu(message.from_user.id))
        else:
            await message.answer(ts("Ви вже зареєстровані.", await get_lang(message.from_user.id)), reply_markup=await display_general_menu(message.from_user.id))
    except Exception as err:
            print(err)


def keyboard_to_dict(keyboard: InlineKeyboardMarkup) -> dict:
    result = []
    for row in keyboard.inline_keyboard:
        row_data = []
        for button in row:
            button_data = {"text": button.text}
            
            if button.url:
                button_data["url"] = button.url
            
            if button.callback_data:
                button_data["callback_data"] = button.callback_data
            
            row_data.append(button_data)
        result.append(row_data)
    return {"inline_keyboard": result}


async def send_message(user: int, text: str, session: Optional[ClientSession] = None, keyboard: Optional[InlineKeyboardMarkup] = None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    params = {
        'chat_id': user,
        'text': text,
        'reply_markup': keyboard_to_dict(keyboard)
    }

    async with session.post(url, json=params) as response:
        if response.status != 200:
            print(f"Failed to send message to {user}: {response.status}")
            response_text = await response.text()
            print(f"Response text: {response_text}")

async def send_notification(ukr_text, en_text, prev_percent_change, now_percent_change, link, minute_analysis, name_coin):
    prev_percent_change = float(prev_percent_change)
    now_percent_change = float(now_percent_change)
    async with aiohttp.ClientSession() as session:
        users = await get_all_users()
        if users != []:
            for user in users:
                if minute_analysis in user.signal_interval and user and ((now_percent_change < 0 and now_percent_change <= user.degreas_percent and abs(prev_percent_change - now_percent_change) >= abs(user.degreas_percent)) or (now_percent_change > 0 and now_percent_change >= user.increas_percent and abs(prev_percent_change - now_percent_change) >= user.increas_percent)):
                    try:
                        if now_percent_change > 200 and abs(prev_percent_change - now_percent_change) < 50:
                            return False
                        keyboard = await display_coin_spot(link, user.tg_id, name_coin)
                        if user.lang == 'ukr':
                            await send_message(user.tg_id, ukr_text, session, keyboard)
                            try:
                                await add_signal_history(ukr_text, user.tg_id)
                            except Exception as err:
                                print(err)
                        else:
                            await send_message(user.tg_id, en_text, session, keyboard)
                            try:
                                await add_signal_history(en_text, user.tg_id)
                            except Exception as err:
                                print(err)
                        await sleep(0.5)
                    except Exception as err:
                        print(f"{user.tg_id}: {err}")
