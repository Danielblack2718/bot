from db import db
from aiogram.dispatcher import Dispatcher
from filters.sub_channel import Channel
from handlers import hand_start
from handlers import hand_admin
from handlers import hand_buy
from handlers import hand_profile
import Keyboards
import User


def setup(dp: Dispatcher):
    dp.filters_factory.bind(Channel)
