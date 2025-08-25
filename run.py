import asyncio

from config import bot, dp
from handlers import handlers_router
from commands import commands_router

async def main():
    dp.include_router(commands_router)
    dp.include_router(handlers_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
