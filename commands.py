import asyncio
import logging
import aiohttp
from aiogram import Router, F
from aiogram.filters import Command

import database
import keyboards
from config import bot

logger = logging.getLogger(__name__)

commands_router = Router()

API_URL = 'https://cataas.com/cat?json=true'
db = database.CatDataBase()


# -------------------------------------------------------------------------------------------------------
async def get_random_cat_url():
    timeout = aiohttp.ClientTimeout(
        total=10,  # Общий таймаут
        connect=3,  # Таймаут подключения
        sock_read=5  # Таймаут чтения
    )

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(API_URL) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['url']
                return
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        logging.error(f"error in get_random_cat_url: {e}")
        return None


async def send_cat(chat_id: int, reply_msg_func, reply_photo_func):
    await bot.send_chat_action(chat_id, 'upload_photo')
    img = await get_random_cat_url()
    if img:
        await reply_photo_func(photo=img,
            caption="добавить в Избранное этого котика?",
            reply_markup=keyboards.rate_cat_kb
        )
    else:
        await reply_msg_func('не получилось загрузить котика 😢')
# -------------------------------------------------------------------------------------------------------
@commands_router.startup()
async def on_startup():
    await db.create_db()

@commands_router.message(Command('cat_picture'))
async def cat_picure_handler(message):
    try:
        await send_cat(message.chat.id, message.answer, message.answer_photo)
    except Exception as e:
        logging.error("error in cat_picture_handler: {e}")
        await message.answer('произошла ошибка при отправке котика 😢')

@commands_router.message(Command('my_favourites'))
async def my_favourites_handler(message):
    try:
        user_id = message.from_user.id
        user_favourites = await db.get_user_favourites(user_id)

        if user_favourites:
            await message.answer('вот последнее фото из Избранные:')
            await message.answer_photo(photo=user_favourites[0])
        else:
            await message.answer('вы не добавили ничего в Избранные!')

    except Exception as e:
        logging.error(f"error in my_favourites_handler: {e}")


@commands_router.callback_query((F.data == 'load') | (F.data == 'no_load'))
async def load_cat_callback(callback):
    try:
        await callback.answer()
        if callback.data == 'load':
            await bot.send_chat_action(callback.message.chat.id, 'typing')
            user_id = callback.from_user.id
            file_id = callback.message.photo[-1].file_id
            success = await db.add_favourites(user_id, file_id)
            if success:
                await callback.message.answer("отлично! я загрузил вашего котика в Избранное ✅")
            else:
                await callback.message.answer("произошла ошибка сохранения ❌")

            TIME_TO_DELAY = 1
            await asyncio.sleep(TIME_TO_DELAY)
            await callback.message.answer('хотите продолжить просмотр котиков? 😽', reply_markup=keyboards.next_cat_kb)
        else:
            await send_cat(callback.message.chat.id, callback.message.answer, callback.message.answer_photo)
    except Exception as e:
        logging.error(f"error in load_cat_callback: {e}")


@commands_router.callback_query((F.data == 'send') | (F.data == 'no_send'))
async def next_cat_callback(callback):
    await callback.answer()
    if callback.data == 'send':
        await send_cat(callback.message.chat.id, callback.message.answer, callback.message.answer_photo)
    else:
        await callback.message.answer('вас понял')
