import datetime
import random
from aiohttp import ClientSession
import Config
from InstanceBot import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from db import db
import Keyboards

import User
from AaioAPI import AsyncAaioAPI


async def usd_to_rub():
    async with ClientSession() as s:
        async with s.get('https://api.coinbase.com/v2/prices/USD-RUB/spot') as res:
            res = await res.json()

            return round(float(res['data']['amount']), 2)


async def choice_category(call: types.CallbackQuery):
    user_id = call.from_user.id
    temp = call.data.split('|')

    if temp[1] == 'next':
        await bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=call.message.message_id,
            reply_markup=Keyboards.category(int(temp[2]))
        )

    elif temp[1] == 'back':
        await bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=call.message.message_id,
            reply_markup=Keyboards.category(int(temp[2]))
        )

    else:
        category = db.get_info_category(temp[1])
        user = db.get_info_user(user_id)

        if category[3] == '0':
            await bot.edit_message_caption(
                chat_id=user_id,
                caption="текст выбора категории {}".format(
                    category[2]
                ),
                message_id=call.message.message_id,
                reply_markup=Keyboards.products(
                    cat_id=temp[1],
                    remover=0,
                    lang=user[3],
                    currency=user[4],
                    usd_to_rub=await usd_to_rub() if user[4] == 'USD' else None
                )
            )
        else:
            await bot.delete_message(user_id, call.message.message_id)

            await bot.send_photo(
                chat_id=user_id,
                photo=category[3],
                caption="текст выбора категории {}".format(
                    category[2]
                ),
                reply_markup=Keyboards.products(
                    cat_id=temp[1],
                    remover=0,
                    lang=user[3],
                    currency=user[4],
                    usd_to_rub=await usd_to_rub() if user[4] == 'USD' else None
                )
            )


async def choice_product(call: types.CallbackQuery):
    user_id = call.from_user.id
    user = db.get_info_user(user_id)
    temp = call.data.split('|')

    if temp[1] == 'next':
        await bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=call.message.message_id,
            reply_markup=Keyboards.products(
                cat_id=temp[3],
                remover=int(temp[2]),
                currency=user[4],
                lang=user[3],
                usd_to_rub=await usd_to_rub() if user[4] == 'USD' else None
            )
        )

    elif temp[1] == 'back':
        await bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=call.message.message_id,
            reply_markup=Keyboards.products(
                cat_id=temp[3],
                remover=int(temp[2]),
                currency=user[4],
                lang=user[3],
                usd_to_rub=await usd_to_rub() if user[4] == 'USD' else None
            )
        )

    elif temp[1] == 'menu':
        await bot.delete_message(user_id, call.message.message_id)

        with open('./photo/products.jpg', 'rb') as photo:
            await bot.send_photo(
                chat_id=user_id,
                photo=photo,
                caption="текст категорий",
                reply_markup=Keyboards.category(0)
            )

    else:
        product = db.get_info_product(temp[2])

        if product[5] == '0':
            await bot.edit_message_caption(
                chat_id=user_id,
                caption="текст выбора продукта {} {} {} {} {} {} {} {}".format(
                    product[3],
                    db.get_info_category(temp[1])[2],
                    len(db.get_remain_product(temp[1], temp[2]))
                    if product[7] == 0 else db.get_remain_product(temp[1], temp[2], adm_product=True),
                    temp[3],
                    user[4],
                    product[6],
                    product[6]
                ),
                message_id=call.message.message_id,
                reply_markup=Keyboards.actions_product(
                    cat_id=temp[1],
                    product_id=temp[2],
                    price=temp[3],
                    lang=user[3]
                )
            )
        else:
            await bot.delete_message(user_id, call.message.message_id)

            await bot.send_photo(
                chat_id=user_id,
                photo=product[5],
                caption="текст выбора продукта {} {} {} {} {} {} {} {}".format(
                    product[3],
                    db.get_info_category(temp[1])[2],
                    len(db.get_remain_product(temp[1], temp[2]))
                    if product[7] == 0 else db.get_remain_product(temp[1], temp[2], adm_product=True),
                    temp[3],
                    user[4],
                    product[6],
                    product[6]
                ),
                reply_markup=Keyboards.actions_product(
                    cat_id=temp[1],
                    product_id=temp[2],
                    price=temp[3],
                    lang=user[3]
                )
            )


async def choice_product_action(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user = db.get_info_user(user_id)
    temp = call.data.split('|')

    if temp[1] == 'back':
        category = db.get_info_category(temp[2])
        user = db.get_info_user(user_id)

        if category[3] == '0':
            await bot.edit_message_caption(
                chat_id=user_id,
                caption="текст выбора категории {}".format(
                    category[2]
                ),
                message_id=call.message.message_id,
                reply_markup=Keyboards.products(
                    cat_id=temp[2],
                    remover=0,
                    lang=user[3],
                    currency=user[4],
                    usd_to_rub=await usd_to_rub() if user[4] == 'USD' else None
                )
            )
        else:
            await bot.delete_message(user_id, call.message.message_id)

            await bot.send_photo(
                chat_id=user_id,
                photo=category[3],
                caption="текст выбора категории {}".format(
                    category[2]
                ),
                reply_markup=Keyboards.products(
                    cat_id=temp[2],
                    remover=0,
                    lang=user[3],
                    currency=user[4],
                    usd_to_rub=await usd_to_rub() if user[4] == 'USD' else None
                )
            )

    else:
        count_product = len(db.get_remain_product(temp[2], temp[3])) \
            if db.get_info_product(temp[3])[7] == 0 else int(db.get_remain_product(temp[2], temp[3], adm_product=True))

        if count_product < 1:
            await call.answer(
                'Товара нет в наличии!'
            )
            return

        await bot.delete_message(user_id, call.message.message_id)

        async with state.proxy() as data:
            data['cat_id'] = temp[2]
            data['product_id'] = temp[3]
            data['price'] = temp[4]

        await User.buy.start.set()
        await bot.send_message(
            chat_id=user_id,
            text="текст количества продуктов {} {} {} {} {}".format(
                db.get_info_product(temp[3])[3],
                temp[4],
                user[4],
                len(db.get_remain_product(temp[2], temp[3]))
                if db.get_info_product(temp[3])[7] == 0 else int(db.get_remain_product(temp[2], temp[3], adm_product=True))
            )
        )


async def get_count(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = db.get_info_user(user_id)

    async with state.proxy() as data:
        cat_id = data['cat_id']
        product_id = data['product_id']
        price = data['price']

    if not message.text.isdigit():
        await message.answer(
            text="текст предупреждения"
        )
        return

    count_product = len(db.get_remain_product(cat_id, product_id)) \
        if db.get_info_product(product_id)[7] == 0 else int(db.get_remain_product(cat_id, product_id, adm_product=True))

    if count_product < int(message.text):
        await message.answer(
            text="текст предупреждения {}".format(
                count_product
            )
        )
        return

    amount = int(price) * int(message.text)

    product = db.get_info_product(product_id)

    async with state.proxy() as data:
        data['count'] = int(message.text)
        data['price'] = amount

    if product[5] == '0':
        await message.answer(
            text="текст подтверждения покупки".format(
                product[3],
                int(message.text),
                amount,
                user[4]
            ),
            reply_markup=Keyboards.accept_buy(
                count=int(message.text),
                amount=price,
                cat_id=cat_id,
                product_id=product_id,
                lang=user[3]
            )
        )
    else:
        await message.answer_photo(
            photo=product[5],
            caption="текст покупки предмета {} {} {} {}".format(
                product[3],
                int(message.text),
                amount,
                user[4]
            ),
            reply_markup=Keyboards.accept_buy(
                count=int(message.text),
                amount=price,
                cat_id=cat_id,
                product_id=product_id,
                lang=user[3]
            )
        )


async def accept_buy(call: types.CallbackQuery):
    user_id = call.from_user.id
    user = db.get_info_user(user_id)
    temp = call.data.split('|')

    if temp[1] == 'y':
        await bot.delete_message(user_id, call.message.message_id)

        with open('./photo/payment.jpg', 'rb') as photo:
            await bot.send_photo(
                photo=photo,
                chat_id=user_id,
                caption="текст выбора платег",
                reply_markup=Keyboards.choice_payment()
            )

    if temp[1] == 'n':
        await bot.delete_message(user_id, call.message.message_id)

        await User.menu.start.set()
        await bot.send_message(
            chat_id=user_id,
            text="начальный текст",
            reply_markup=Keyboards.menu(user[3])
        )


async def choice_payment(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user = db.get_info_user(user_id)
    temp = call.data.split('|')

    async with state.proxy() as data:
        product_id = data['product_id']
        price = data['price']
        count = data['count']

    if temp[1] == 'aaio':
        aaio = AsyncAaioAPI(
            API_KEY=Config.api_key_aaio,
            SECRET_KEY=Config.secret_key_aaio,
            MERCHANT_ID=Config.merchant_id_aaio
        )

        order_id = ''.join([str(random.randint(1, 9)) for _ in range(10)])

        pay_url = await aaio.create_payment(
            order_id=order_id,
            amount=price,
            currency=user[4]
        )

        await User.buy.check.set()
        await bot.edit_message_caption(
            chat_id=user_id,
            caption="текст проверки платежа/платеги".format(
                db.get_info_product(product_id)[3],
                count,
                price,
                user[4]
            ),
            message_id=call.message.message_id,
            reply_markup=Keyboards.check_payment(pay_url, order_id, user[3])
        )


async def check_payment(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user = db.get_info_user(user_id)
    temp = call.data.split('|')

    if temp[1] == 'cancel':
        await bot.delete_message(user_id, call.message.message_id)

        await bot.send_message(
            chat_id=user_id,
            text="Начальный текст",
            reply_markup=Keyboards.menu(user[3])
        )

    else:
        aaio = AsyncAaioAPI(
            API_KEY=Config.api_key_aaio,
            SECRET_KEY=Config.secret_key_aaio,
            MERCHANT_ID=Config.merchant_id_aaio
        )

        if await aaio.is_expired(temp[1]):
            await call.answer(
                "текст проверки платежа/платеги"
            )

            await bot.delete_message(user_id, call.message.message_id)

            await bot.send_message(
                chat_id=user_id,
                text="Начальный текст",
                reply_markup=Keyboards.menu(user[3])
            )
            return

        if await aaio.is_success(temp[1]):
            await call.answer(
                "текст проверки платежа/платеги"
            )
            return

        await bot.delete_message(user_id, call.message.message_id)

        async with state.proxy() as data:
            cat_id = data['cat_id']
            product_id = data['product_id']
            price = data['price']
            count = data['count']

        product = db.get_info_product(product_id)

        if product[7] == 0:
            remains = [i[3] for i in db.get_remain_product(cat_id, product_id)]

            product_text = f'текст покупки предмета\n'

            for a, _ in enumerate(range(count)):
                product_text += f'<code>{remains[a]}</code>\n'
                db.delete_remains(remains[a])

            await User.menu.start.set()
            await bot.send_message(
                chat_id=user_id,
                text=product_text,
                reply_markup=Keyboards.menu(user[3])
            )

        else:
            remains = "текст покупки предмета"

            db.delete_remains(cat_id=cat_id, product_id=product_id, count=count)

            await User.menu.start.set()
            await bot.send_message(
                chat_id=user_id,
                text=remains,
                reply_markup=Keyboards.menu(user[3])
            )

        db.add_order(
            temp[1],
            user_id,
            price,
            (datetime.datetime.now()).strftime('%Y-%m-%d'),
            product[3]
        )

        await bot.send_message(
            chat_id=Config.admins[0],
            text=f'<b>Покупка товара.</b>\n\n'
                 f'<b>Товар:</b> {product[3]}\n'
                 f'<b>Кол-во:</b> {count}\n'
                 f'<b>Сумма оплаты:</b> {price} {user[4]}\n\n'
                 f'<b>ID:</b> {user_id}\n'
                 f'<b>UN:</b> @{call.from_user.username}'
        )


def hand_add(dp: Dispatcher):
    dp.register_callback_query_handler(choice_category, lambda c: c.data and c.data.startswith('r'), state='*')
    dp.register_callback_query_handler(choice_product, lambda c: c.data and c.data.startswith('s'), state='*')
    dp.register_callback_query_handler(choice_product_action, lambda c: c.data and c.data.startswith('b'), state='*')

    dp.register_message_handler(get_count, content_types=['text'], state=User.buy.start)
    dp.register_callback_query_handler(accept_buy, lambda c: c.data and c.data.startswith('c'), state=User.buy.start)
    dp.register_callback_query_handler(choice_payment, lambda c: c.data and c.data.startswith('y'),
                                       state=User.buy.start)
    dp.register_callback_query_handler(check_payment, lambda c: c.data and c.data.startswith('check'),
                                       state=User.buy.check)
