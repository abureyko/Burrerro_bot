import logging
import random

from aiogram import F, Router
from aiogram.filters import CommandStart
from emoji import is_emoji

handlers_router = Router()
logging.basicConfig(level=logging.INFO)

UNKNOWN_RESPONSES = [
    'я пока только учусь понимать такие сообщения 🤨',
    'моя твоя не понимать...',
    'этому меня еще не научили :(',
    'это ваще че 😮'
]

@handlers_router.message(CommandStart())
async def command_start_handler(message):
    await message.answer('привет, я обожаю котов!!')


@handlers_router.message(F.sticker)
async def sticker_handler(message):
    await message.answer('хахахаха, прикольный стик 👍🏻')


@handlers_router.message(F.text.func(lambda s: any(is_emoji(c) for c in s)))
async def emoji_handler(message):
    await message.answer('забавный эмодзи :P')


@handlers_router.message(F.photo | F.video)
async def photo_handler(message):
    await message.answer('потрясающая у тебя галерея 📷')


@handlers_router.message(F.voice | F.video_note)
async def media_message_handler(message):
    if message.voice:
        await message.answer('какой красивый голос 😻')
    else:
        await message.answer('крутой кружок !!')


@handlers_router.message()
async def message_handler(message):
    await message.answer(random.choice(UNKNOWN_RESPONSES))
