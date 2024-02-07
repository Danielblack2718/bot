from aiogram.dispatcher import Dispatcher
from sub_channel import Channel


def setup(dp: Dispatcher):
    dp.filters_factory.bind(Channel)
