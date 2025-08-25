import asyncio
import logging

import aiohttp
from aiogram import Router, F
from aiogram.filters import Command

import keyboards
from config import bot

commands_router = Router()
logging.basicConfig(level=logging.INFO)


API_URL = 'https://cataas.com/cat?json=true'


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
                    return f"https://cataas.com{data['url']}"
                return
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        logging.error(f"ошибка при получении котика: {e}")
        return None

async def send_cat(chat_id: int, reply_msg_func, reply_photo_func):
    await bot.send_chat_action(chat_id, 'upload_photo')
    img = await get_random_cat_url()
    if img:
        await reply_photo_func(photo=img)
        await reply_msg_func('добавить в избранные этого котика?', reply_markup=keyboards.rate_cat_kb)
    else:
        await reply_msg_func('не получилось загрузить котика 😢')




@commands_router.message(Command('cat_pic'))
async def cat_pic_handler(message):
    await send_cat(message.chat.id, message.answer, message.answer_photo)

@commands_router.callback_query((F.data == 'load') | (F.data == 'no_load'))
async def load_cat_callback(callback):
    await callback.answer()
    if callback.data == 'load':
        #load to database function
        await callback.message.answer("отлично! я загрузил вашего котика в избранные 🗂")
        await callback.message.answer('хотите продолжить просмотр котиков? 😽', reply_markup=keyboards.next_cat_kb)
    else:
        await send_cat(callback.message.chat.id, callback.message.answer, callback.message.answer_photo)

@commands_router.callback_query((F.data == 'send') | (F.data=='no_send'))
async def next_cat(callback):
    await callback.answer()
    if callback.data == 'send':
        await send_cat(callback.message.chat.id, callback.message.answer, callback.message.answer_photo)
    else:
        await callback.message.answer('вас понял')