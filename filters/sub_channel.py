from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
import Config
from InstanceBot import bot
import Keyboards


class Channel(BoundFilter):
    def __init__(self, yes_sub):
        self.yes_sub = yes_sub

    async def check(self, message: types.Message):
        user_id = message.from_user.id

        user_channel = await bot.get_chat_member(
            chat_id=Config.admin_channel,
            user_id=user_id
        )

        if user_channel['status'] != 'left':
            return self.yes_sub

        await bot.send_message(
            chat_id=user_id,
            text='Подпишитесь на канал прежде чем продолжить!',
            reply_markup=Keyboards.channel()
        )
