from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile
from datetime import datetime
from aiogram.fsm.context import FSMContext
from datebase.user import get_user_info, set_degreas_percent, set_increas_percent, get_lang, change_lang, set_signal_interval, delete_signal_interval, bind_mail
from keyboards.reply import display_threshold_increas_settings, display_threshold_degreas_settings, display_general_menu, display_select_language_menu, display_signal_settings, display_interval_settings
from utils.settings import Form
from translate import translate as ts
import os
from re import match
from reports_handler import create_report

EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"

router = Router()


@router.message((F.text.lower() == "отримати звіт") | ((F.text.lower() == "get report")))
async def signal_interval_settings(message: Message, bot: Bot, state: FSMContext):
    try:
        userInfo = await get_user_info(message.from_user.id)
        if userInfo is not None:
            text = userInfo.signals_history
            pdf_file_path = create_report(text, message.from_user.id)

            await message.reply_document(FSInputFile(pdf_file_path))

            os.remove(pdf_file_path)
    except Exception as err:
        print(err)

@router.message((F.text.lower() == "прив'язати пошту") | ((F.text.lower() == "bind mail")))
async def mail_settings(message: Message, bot: Bot, state: FSMContext):
    try:
        userInfo = await get_user_info(message.from_user.id)
        if userInfo is not None:
            await message.answer(ts("Введіть пошту.", await get_lang(message.from_user.id)))
            await state.set_state(Form.change_mail)
    except Exception as err:
     print(err)

@router.message((F.text.lower() == "часові проміжки сигналів") | ((F.text.lower() == "time intervals of signals")))
async def signal_interval_settings(message: Message, bot: Bot, state: FSMContext):
    try:
        userInfo = await get_user_info(message.from_user.id)
        if userInfo is not None:
            await message.answer(ts("Ви можете встановити інтервали, за які будуть братись зміни ціни монет.", await get_lang(message.from_user.id)), reply_markup=await display_interval_settings(userInfo.signal_interval, message.from_user.id))
            await state.set_state(Form.change_signal_interval)
    except Exception as err:
     print(err)

@router.message((F.text.lower() == "мінімальний відсоток при зростанні") | ((F.text.lower() == "the minimum percentage during growth")))
async def threshold_ancreas_settings(message: Message, bot: Bot, state: FSMContext):
    try:
        userInfo = await get_user_info(message.from_user.id)
        if userInfo is not None:
            await message.answer(ts("Ви можете встановити мінімальний відсоток при зростанні монети.\nВи отримуватимете інформацію про монети, які зросли на цей відсоток, або вище сьогодні.", await get_lang(message.from_user.id)), reply_markup=await display_threshold_increas_settings(userInfo.increas_percent, message.from_user.id))
            await state.set_state(Form.change_threshold_ancreas)
    except Exception as err:
     print(err)

@router.message((F.text.lower() == "мінімальний відсоток при падінні") | (F.text.lower() == "minimum percentage when falling"))
async def threshold_degreas_settings(message: Message, bot: Bot, state: FSMContext):
    try:
        userInfo = await get_user_info(message.from_user.id)
        if userInfo is not None:
            await message.answer(ts("Ви можете встановити мінімальний відсоток при падінні монети.\nВи отримуватимете інформацію про монети, які впали на цей відсоток, або вище сьогодні.", await get_lang(message.from_user.id)), reply_markup=await display_threshold_degreas_settings(userInfo.degreas_percent, message.from_user.id))
            await state.set_state(Form.change_threshold_degreas)
    except Exception as err:
     print(err)

@router.message((F.text.lower() == "головне меню") | (F.text.lower() == "general menu"))
async def general_menu(message: Message, bot: Bot):
    try:
        await message.answer(ts("Ви успішно повернулись в головне меню.", await get_lang(message.from_user.id)), reply_markup=await display_general_menu(message.from_user.id))
    except Exception as err:
     print(err)

@router.message((F.text.lower() == "налаштування сигналів") | (F.text.lower() == "signal settings"))
async def signal_settings(message: Message, bot: Bot):
    try:
        await message.answer(ts("Налаштування сигналів успішно відкрито.", await get_lang(message.from_user.id)), reply_markup=await display_signal_settings(message.from_user.id))
    except Exception as err:
     print(err)

@router.message((F.text.lower() == "змінити мову") | (F.text.lower() == "change language"))
async def change_name(message: Message, state: FSMContext):
    try:
        await state.set_state(Form.change_lang)
        await message.answer(ts("Виберіть мову.", await get_lang(message.from_user.id)), reply_markup=display_select_language_menu())
    except Exception as err:
        print(err)




@router.message(Form.change_lang)
async def change_name_(message: Message, state: FSMContext):
    try:
        if message.text == 'English':
            lang = 'en'
        elif message.text == 'Українська':
            lang = 'ukr'
        if await change_lang(message.from_user.id, lang):
            await message.answer(ts("Ви успішно змінили мову.", await get_lang(message.from_user.id)), reply_markup=await display_general_menu(message.from_user.id))
        else:
            await message.answer(ts("Сталась помилка, спробуйте пізніше.", await get_lang(message.from_user.id)), reply_markup=await display_general_menu(message.from_user.id))
        await state.clear()
    except Exception as err:
        print(err)

@router.message(Form.change_threshold_ancreas)
async def change_threshold_ancreas_(message: Message, state: FSMContext):
    try:
        if message.text.lower() == "скасувати" or message.text.lower() == "cancel":
            await state.clear()
            await message.answer(ts("Налаштування сигналів успішно відкрито.", await get_lang(message.from_user.id)), reply_markup=await display_signal_settings(message.from_user.id))
        else:
            text = message.text
            parts = text.split(" ")
            if (len(parts) == 2 and parts[0].strip() == "Встановити") or (len(parts) == 2 and parts[0].strip() == "Install"):
                percent = parts[1].strip()
                percent = int(percent)
                if percent in [5, 10, 20]:
                    try:
                        result = await set_increas_percent(percent, message.from_user.id)

                        if result:
                            await message.answer(f"{ts('Ви успішно встановили поріг', await get_lang(message.from_user.id))} {percent}%.", reply_markup=await display_general_menu(message.from_user.id))
                            await state.clear()
                        else:
                            await message.answer(f"{ts('Ви вже використовуєте поріг', await get_lang(message.from_user.id))} {percent}%.")  
                    except ValueError:
                        await message.answer(ts("Введіть корректне число.", await get_lang(message.from_user.id)))
    except Exception as err:
        print(err)

@router.message(Form.change_threshold_degreas)
async def change_threshold_degreas_(message: Message, state: FSMContext):
    try:
        if message.text.lower() == "скасувати" or message.text.lower() == "cancel":
            await state.clear()
            await message.answer(ts("Налаштування сигналів успішно відкрито.", await get_lang(message.from_user.id)), reply_markup=await display_signal_settings(message.from_user.id))
        else:
            text = message.text
            parts = text.split(" ")
            if (len(parts) == 2 and parts[0].strip() == "Встановити") or (len(parts) == 2 and parts[0].strip() == "Install"):
                percent = parts[1].strip()
                percent = int(percent)
                if percent in [-5, -10, -20]:
                    try:
                        result = await set_degreas_percent(percent, message.from_user.id)

                        if result:
                            await message.answer(f"{ts('Ви успішно встановили поріг', await get_lang(message.from_user.id))} {percent}%.", reply_markup=await display_general_menu(message.from_user.id))
                            await state.clear()
                        else:
                            await message.answer(f"{ts('Ви вже використовуєте поріг', await get_lang(message.from_user.id))} {percent}%.")  
                    except ValueError:
                        await message.answer(ts("Введіть корректне число.", await get_lang(message.from_user.id)))
    except Exception as err:
        print(err)

@router.message(Form.change_signal_interval)
async def change_signal_interval_(message: Message, state: FSMContext):
    try:
        if message.text.lower() == "скасувати" or message.text.lower() == "cancel":
            await state.clear()
            await message.answer(ts("Налаштування сигналів успішно відкрито.", await get_lang(message.from_user.id)), reply_markup=await display_signal_settings(message.from_user.id))
        else:
            text = message.text
            parts = text.split(" ")
            if (len(parts) == 2 and parts[0].strip() == "Встановити") or (len(parts) == 2 and parts[0].strip() == "Install"):
                interval = parts[1].strip()
                interval = int(interval)
                try:
                    if interval in [5, 15, 45, 60, 135, 240, 540, 1440]:
                        result = await set_signal_interval(interval, message.from_user.id)

                        if result:
                            await message.answer(f"{ts('Ви успішно встановили інтервал', await get_lang(message.from_user.id))} {interval}%.", reply_markup=await display_general_menu(message.from_user.id))
                            await state.clear()
                        else:
                            await message.answer(ts('Інтервал вже використовується', await get_lang(message.from_user.id)))  
                except ValueError:
                    await message.answer(ts("Введіть корректне число.", await get_lang(message.from_user.id)))
            elif (len(parts) == 2 and parts[0].strip() == "Видалити") or (len(parts) == 2 and parts[0].strip() == "Uninstall"):
                interval = parts[1].strip()
                interval = int(interval)
                try:
                    if interval in [5, 15, 45, 60, 135, 240, 540, 1440]:
                        result = await delete_signal_interval(interval, message.from_user.id)

                        if result:
                            await message.answer(f"{ts('Ви успішно видалили інтервал', await get_lang(message.from_user.id))} {interval}.", reply_markup=await display_general_menu(message.from_user.id))
                            await state.clear()
                        else:
                            await message.answer(ts('Інтервал не використовується', await get_lang(message.from_user.id)))  
                except ValueError:
                    await message.answer(ts("Введіть корректне число.", await get_lang(message.from_user.id)))
    except Exception as err:
        print(err)

@router.message(Form.change_mail)
async def change_mail_(message: Message, state: FSMContext):
    try:
        email = message.text.strip()
        if match(EMAIL_REGEX, email) and len(email) > 5 and len(email) < 254:
            await message.answer(ts("Пошту успішно прив`язно.", await get_lang(message.from_user.id)))
            await bind_mail(email, message.from_user.id)
            await state.clear()
        else:
            await message.answer(ts("Неправильний формат пошти. Спробуйте ще раз.", await get_lang(message.from_user.id)))
    except Exception as err:
        print(err)
