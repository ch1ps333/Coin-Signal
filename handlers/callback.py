from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from datebase.user import get_user_info, add_fav_coin
from translate import translate as ts

router = Router()

@router.callback_query(lambda querry: querry.data.startswith("add_fav_"))
async def moreInfo(callback: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        coin = (callback.data.split('_')[2])
        userInfo = await get_user_info(callback.from_user.id)
        if userInfo is not None:
            result = await add_fav_coin(coin, callback.from_user.id)

            if result:
                await callback.answer(ts("Монету успішно додано до обраних.", userInfo.lang))
            else:
                await callback.answer(ts("Монета вже знаходиться в обраних.", userInfo.lang))

    except Exception as err:
        print(err)