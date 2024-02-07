from InstanceBot import bot
from aiogram import types, Dispatcher
from db import db
import Keyboards


async def history_payment(call: types.CallbackQuery):
    user_id = call.from_user.id

    await call.answer()

    await bot.send_message(
        chat_id=user_id,
        text=db.get_user_history_orders(user_id)
    )


async def change_language(call: types.CallbackQuery):
    user_id = call.from_user.id
    user = db.get_info_user(user_id)

    await call.answer()

    if user[3] == 'ru':
        db.update_lang(user_id, 'en')
    else:
        db.update_lang(user_id, 'ru')

    user = db.get_info_user(user_id)
    await bot.send_message(
        chat_id=user_id,
        text='✅',
        reply_markup=Keyboards.menu(user[3])
    )
    await bot.edit_message_text(
        chat_id=user_id,
        text="текст профиля {} {} {}".format(
                user[1],
                db.get_order_user(user[1]),
                user[2]
            ),
        message_id=call.message.message_id,
        reply_markup=Keyboards.profile(user[3])
    )


async def change_currency(call: types.CallbackQuery):
    user_id = call.from_user.id
    user = db.get_info_user(user_id)

    await call.answer('✅')

    if user[4] == 'RUB':
        db.update_currency(user_id, 'USD')
    else:
        db.update_currency(user_id, 'RUB')


def hand_add(dp: Dispatcher):
    dp.register_callback_query_handler(history_payment, lambda c: c.data and c.data.startswith('3history'), state='*')
    dp.register_callback_query_handler(change_language, lambda c: c.data and c.data.startswith('1language'), state='*')
    dp.register_callback_query_handler(change_currency, lambda c: c.data and c.data.startswith('2currency'), state='*')
