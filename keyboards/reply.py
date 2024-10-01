from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from datebase.user import get_lang
from translate import translate as ts


async def display_general_menu(tg_id):
    general_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=ts("Отримати звіт", await get_lang(tg_id)))
            ],
            [
                KeyboardButton(text=ts("Налаштування сигналів", await get_lang(tg_id)))
            ],
            [
                KeyboardButton(text=ts("Змінити мову", await get_lang(tg_id))),
                KeyboardButton(text=ts("Прив'язати пошту", await get_lang(tg_id))),
            ],
        ],
        resize_keyboard=True
    )

    return general_keyboard

async def display_signal_settings(tg_id):
    general_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=ts("Головне меню", await get_lang(tg_id)))
            ],
            [
                KeyboardButton(text=ts("Мінімальний відсоток при зростанні", await get_lang(tg_id))),
                KeyboardButton(text=ts("Мінімальний відсоток при падінні", await get_lang(tg_id)))
            ],
            [
                KeyboardButton(text=ts("Часові проміжки сигналів", await get_lang(tg_id))),
                KeyboardButton(text=ts("Крок між сигналами", await get_lang(tg_id)))
            ],
        ],
        resize_keyboard=True
    )

    return general_keyboard


def display_select_language_menu():
    langKeyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="English"),
                KeyboardButton(text="Українська")
            ],
        ],
        resize_keyboard=True
    )

    return langKeyboard

async def display_threshold_increas_settings(increas_percent, tg_id):
    try:
        builder = ReplyKeyboardBuilder()
        
        builder.row(KeyboardButton(text=ts("Скасувати", await get_lang(tg_id))))

        row_buttons = []
        for number in range(20, 101, 5):
            action = ts("Встановлено", await get_lang(tg_id)) if number == increas_percent else ts("Встановити", await get_lang(tg_id))
            button_text = f"{action} {number}"
            row_buttons.append(KeyboardButton(text=button_text))
            
            if len(row_buttons) == 2:
                builder.row(*row_buttons)
                row_buttons = []
        
        if row_buttons:
            builder.row(*row_buttons)

        return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    
    except Exception as err:
        print(err)
        return builder.as_markup()
    
    
async def display_threshold_degreas_settings(degreas_percent, tg_id):
    try:
        builder = ReplyKeyboardBuilder()
        
        builder.row(KeyboardButton(text=ts("Скасувати", await get_lang(tg_id))))

        row_buttons = []
        for number in range(-20, -101, -5):
            action = ts("Встановлено", await get_lang(tg_id)) if number == degreas_percent else ts("Встановити", await get_lang(tg_id))
            button_text = f"{action} {number}"
            row_buttons.append(KeyboardButton(text=button_text))
            
            if len(row_buttons) == 2:
                builder.row(*row_buttons)
                row_buttons = []
        
        if row_buttons:
            builder.row(*row_buttons)

        return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    
    except Exception as err:
        print(err)
        return builder.as_markup()
    
async def display_step_settings(step, tg_id):
    try:
        builder = ReplyKeyboardBuilder()
        
        builder.row(KeyboardButton(text=ts("Скасувати", await get_lang(tg_id))))

        row_buttons = []
        for number in range(1, 21, 1):
            action = ts("Встановлено", await get_lang(tg_id)) if number == step else ts("Встановити", await get_lang(tg_id))
            button_text = f"{action} {number}"
            row_buttons.append(KeyboardButton(text=button_text))
            
            if len(row_buttons) == 2:
                builder.row(*row_buttons)
                row_buttons = []
        
        if row_buttons:
            builder.row(*row_buttons)

        return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    
    except Exception as err:
        print(err)
        return builder.as_markup()

async def display_interval_settings(intervals, tg_id):
    try:
        builder = ReplyKeyboardBuilder()
        
        builder.row(KeyboardButton(text=ts("Скасувати", await get_lang(tg_id))))

        row_buttons = []
        for number in [5, 15, 45, 60, 135, 240, 540, 1440]:
            action = ts("Видалити", await get_lang(tg_id)) if number in intervals else ts("Встановити", await get_lang(tg_id))
            button_text = f"{action} {number}"
            row_buttons.append(KeyboardButton(text=button_text))
            
            if len(row_buttons) == 2:
                builder.row(*row_buttons)
                row_buttons = []
        
        if row_buttons:
            builder.row(*row_buttons)

        return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    
    except Exception as err:
        print(err)
        return builder.as_markup()