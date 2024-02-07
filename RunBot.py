from aiogram.utils import executor
from aiogram.types import BotCommand
from db import Database
from InstanceBot import bot, dp
import handlers
import filters

async def on_startup(dp):
    db = Database()

    db.create_tables()
    filters.setup(dp)

    bot_commands = [
        BotCommand(command="/start", description="Перезапустить бота")
    ]

    await bot.set_my_commands(bot_commands)
    print('Бот запущен')

    handlers.hand_start.hand_add(dp)
    handlers.hand_buy.hand_add(dp)
    handlers.hand_admin.hand_add(dp)
    handlers.hand_profile.hand_add(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
