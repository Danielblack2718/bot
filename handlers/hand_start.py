import datetime

import Config
from InstanceBot import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from db import db
import Keyboards
import User
from filters.sub_channel import Channel


async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if not db.user_exists(user_id):
        # start_message = message.text[7:]
        #
        # if len(start_message) > 0:
        #     if start_message.isdigit() and start_message != str(user_id):
        #
        #         async with state.proxy() as data:
        #             data['ref_tag'] = start_message
        await bot.send_message(
            chat_id=user_id,
            text="хз какой текст",
            reply_markup=Keyboards.lan()
        )
        return

    user = db.get_info_user(user_id)
    await User.menu.start.set()
    await message.answer(
        text='⏳',
        reply_markup=Keyboards.menu(user[3])
    )
    await message.answer(
        text="начальный текст"
    )


async def choice_lang(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    temp = call.data.split('|')
    now = datetime.datetime.now()

    await bot.delete_message(user_id, call.message.message_id)

    if not db.user_exists(user_id):
        # try:
        #     async with state.proxy() as data:
        #         ref_tag = data['ref_tag']
        #
        # except KeyError:
        #     ref_tag = None

        db.add_user(user_id, now.strftime('%Y-%m-%d'), temp[1])

        # await bot.send_message(
        #     chat_id=Config.admin_channel,
        #     text=f'<b>Новый пользователь:</b>\n'
        #          f'<b>ID:</b> <code>{user_id}</code>\n'
        #          f'<b>UN:</b> @{call.from_user.username}\n'
        #          f'<b>PREM:</b> {call.from_user.is_premium}\n'
        #          f'<b>GEO:</b> {temp[1]}'
        # )

    user = db.get_info_user(user_id)
    await bot.send_message(
        chat_id=user_id,
        text='⏳',
        reply_markup=Keyboards.menu(user[3])
    )
    await User.menu.start.set()
    await bot.send_message(
        chat_id=user_id,
        text="Начальный текст",
        reply_markup=Keyboards.category(0)
    )


async def menu(message: types.Message):
    user = db.get_info_user(message.from_user.id)

    if message.text == '🛍 Товары 🛍':
        with open('./photo/products.jpg', 'rb') as photo:
            await message.answer_photo(
                photo=photo,
                caption="Текст вашей категории товаров",
                reply_markup=Keyboards.category(0)
            )

    if message.text == '👤 Профиль 👤':
        await message.answer(
            text="Текст вашего профиля: {}, {}, {}".format(
                user[1],
                db.get_order_user(user[1]),
                user[2]
            ),
            reply_markup=Keyboards.profile(user[3])
        )

    if message.text == '📝 Отзывы 📝':
        with open('./photo/reviews.jpg', 'rb') as photo:
            await message.answer_photo(
                photo=photo,
                caption="Текст вашего отзыва",

                reply_markup=Keyboards.reviews()
            )

    if message.text == '☎ Поддержка ☎':
        await message.answer(
            text="Текст вашего поддрежки",
            reply_markup=Keyboards.support(user[3])
        )

    if message.text == '❓ FAQ ❓':
        with open('./photo/faq.jpg', 'rb') as photo:
            await message.answer_photo(
                photo=photo,
                caption="FAQ",
                reply_markup=Keyboards.faq()
            )


def hand_add(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state='*')
    dp.register_callback_query_handler(choice_lang, lambda c: c.data and c.data.startswith('lang'), state='*')
    dp.register_message_handler(menu, text=[
        '🛍 Товары 🛍', '🛍 Products 🛍',
        '👤 Профиль 👤', '👤 Profile 👤',
        '📝 Отзывы 📝', '📝 Reviews 📝',
        '☎ Поддержка ☎', '☎ Support ☎',
        '❓ FAQ ❓'
    ], state='*')
