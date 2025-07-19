import asyncio
import logging

import aiohttp
from aiogram import Router, F
from aiogram.filters import Command

import keyboards
from config import bot

main_handlers_router = Router()
logging.basicConfig(level=logging.INFO)

UNKNOWN_RESPONSES = [
    'я пока только учусь понимать такие сообщения 🤨',
    'моя твоя не понимать...',
    'этому меня еще не научили :(',
    'это ваще че 😮'
]

API_URL = 'https://cataas.com/cat?json=true'


# -------------------------------------------------------------------------------------------------------

async def send_cat(chat_id: int, reply_msg_func, reply_photo_func):
    await bot.send_chat_action(chat_id, 'upload_photo')
    img = await get_random_cat_url()
    if img:
        await reply_photo_func(photo=img)
        await asyncio.sleep(2)
        await reply_msg_func('добавить в избранное этого котика?', reply_markup=keyboards.rate_cat_kb)
    else:
        await reply_msg_func('не получилось загрузить котика 😢')


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
        logging.error(f"Ошибка при получении котика: {e}")
        return None


@main_handlers_router.message(Command('cat_pic'))
async def cat_pic_handler(message):
    await send_cat(message.chat.id, message.answer, message.answer_photo)

@main_handlers_router.callback_query(F.data == 'load_cat')
async def load_cat_callback(callback):
    await callback.answer()
    #тут надо написать функционал для загрузки котов в избранное пользователя(data base)

@main_handlers_router.callback_query(F.data == 'no_load')
async def no_load(callback):
    await callback.answer()
    #тут надо отправить сообщение пользователю и предложить прислать еще кота