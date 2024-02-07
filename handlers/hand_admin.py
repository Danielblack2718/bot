import asyncio
import os
import aiogram
import Config
from InstanceBot import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from db import db
import Keyboards
import User


async def admin(message: types.Message):
    user_id = message.from_user.id

    if user_id in Config.admins:
        if message.text == '/adm':
            await User.admin.start.set()
            await message.answer(
                text=f'<b>Админ меню</b>\n\n'
                     f'<b>👤 Пользователи:</b>\n'
                     f'День: {db.get_users()[0]}\n'
                     f'Неделя: {db.get_users()[1]}\n'
                     f'Месяц: {db.get_users()[2]}\n'
                     f'Всего: {len(db.get_users()[3])}',
                reply_markup=Keyboards.admin_menu()
            )


async def choice(call: types.CallbackQuery):
    user_id = call.from_user.id
    temp = call.data.split('|')

    if temp[1] == 'mail':
        await User.admin.mail_text.set()
        await bot.edit_message_text(
            chat_id=user_id,
            text='Введите текст рассылки, разметка HTML.',
            message_id=call.message.message_id
        )

    if temp[1] == 'category':
        await call.answer()

        await User.admin.add_cat.set()
        await bot.send_message(
            chat_id=user_id,
            text='Введите название категории'
        )

    if temp[1] == 'change_cat':
        await User.admin.change_cat.set()
        await bot.edit_message_text(
            chat_id=user_id,
            text='Выберите категорию:',
            message_id=call.message.message_id,
            reply_markup=Keyboards.category(0, adm=True)
        )

    if temp[1] == 'product':
        await User.admin.add_sub.set()
        await bot.edit_message_text(
            chat_id=user_id,
            text='Выберите категорию для добавления товара:',
            message_id=call.message.message_id,
            reply_markup=Keyboards.category(0, adm=True)
        )

    if temp[1] == 'change_product':
        await User.admin.change_sub.set()
        await bot.edit_message_text(
            chat_id=user_id,
            text='Выберите нужный товар:',
            message_id=call.message.message_id,
            reply_markup=Keyboards.adm_products(0)
        )

    if temp[1] == 'add_products':
        await User.admin.add_product.set()
        await bot.edit_message_text(
            chat_id=user_id,
            text='Выберите нужный товар:',
            message_id=call.message.message_id,
            reply_markup=Keyboards.adm_products(0)
        )


#######################
async def get_category_name(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['cat_name'] = message.text

    await User.admin.add_cat_photo.set()
    await message.answer(
        text='Отправьте фото для категории, если фото не нужно - отправьте любой символ.'
    )


async def get_category_photo(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        cat_name = data['cat_name']

    if message.photo:
        db.add_category(cat_name, message.photo[-1].file_id)

    else:
        db.add_category(cat_name, 0)

    await User.admin.start.set()
    await message.answer(
        f'Категория {cat_name} добавлена!',
        reply_markup=Keyboards.admin_menu()
    )


async def choice_cat(call: types.CallbackQuery):
    user_id = call.from_user.id
    temp = call.data.split('|')

    if temp[1] == 'next':
        await bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=call.message.message_id,
            reply_markup=Keyboards.category(int(temp[2]), adm=True)
        )

    elif temp[1] == 'back':
        await bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=call.message.message_id,
            reply_markup=Keyboards.category(int(temp[2]), adm=True)
        )

    elif temp[1] == 'menu':
        await User.admin.start.set()
        await bot.edit_message_text(
            chat_id=user_id,
            text='Админ-меню',
            message_id=call.message.message_id,
            reply_markup=Keyboards.admin_menu()
        )

    else:
        await bot.edit_message_text(
            chat_id=user_id,
            text='Выберите настройку:',
            message_id=call.message.message_id,
            reply_markup=Keyboards.change_cat(temp[1])
        )


async def change_cat(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    temp = call.data.split('|')

    if temp[1] == 'cat_name':
        await call.answer()

        async with state.proxy() as data:
            data['cat_id'] = temp[2]

        await User.admin.change_cat_name.set()
        await bot.send_message(
            chat_id=user_id,
            text='Введите новое название категории'
        )

    if temp[1] == 'del':
        db.delete_category(temp[2])

        await User.admin.change_cat.set()
        await bot.edit_message_text(
            chat_id=user_id,
            text='Выберите категорию:',
            message_id=call.message.message_id,
            reply_markup=Keyboards.category(0, adm=True)
        )

    if temp[1] == 'back':
        await User.admin.change_cat.set()
        await bot.edit_message_text(
            chat_id=user_id,
            text='Выберите категорию:',
            message_id=call.message.message_id,
            reply_markup=Keyboards.category(0, adm=True)
        )


async def update_cat_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        cat_id = data['cat_id']

    db.update_cat_name(cat_id, message.text)

    await User.admin.change_cat.set()
    await message.answer(
        text='Значение изменено!',
        reply_markup=Keyboards.category(0, adm=True)
    )


#########################
async def choice_category(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    temp = call.data.split('|')

    if temp[1] == 'next':
        await bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=call.message.message_id,
            reply_markup=Keyboards.category(int(temp[2]), adm=True)
        )

    elif temp[1] == 'back':
        await bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=call.message.message_id,
            reply_markup=Keyboards.category(int(temp[2]), adm=True)
        )

    elif temp[1] == 'menu':
        await User.admin.start.set()
        await bot.edit_message_text(
            chat_id=user_id,
            text='Админ-меню',
            message_id=call.message.message_id,
            reply_markup=Keyboards.admin_menu()
        )

    else:
        await call.answer()

        async with state.proxy() as data:
            data['cat_id'] = temp[1]

        await bot.send_message(
            chat_id=user_id,
            text='Отправьте данные о товаре:\n'
                 'НАЗВАНИЕ\n'
                 'ЦЕНА В РУБ\n'
                 'ССЫЛКА НА ОПИСАНИЕ (если нет, ссылку на бота)\n'
                 'ТИП ТОВАРА (Если нужна выдача админом > 1, если нет > 0)'
        )


async def get_product_info(message: types.Message, state: FSMContext):
    product_info = message.text.split('\n')

    async with state.proxy() as data:
        data['product_name'] = product_info[0]
        data['product_cost'] = product_info[1]
        data['product_url'] = product_info[2]
        data['product_type'] = product_info[3]

    if len(product_info) < 4:
        await message.answer(
            text='Что-то забыл указать...'
        )
        return

    await User.admin.add_sub_photo.set()
    await message.answer(
        text='Отправьте фото товара, если фото нет - отправьте любой символ.'
    )


async def get_product_photo(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        cat_id = data['cat_id']
        product_name = data['product_name']
        product_cost = data['product_cost']
        product_url = data['product_url']
        product_type = data['product_type']

    if message.photo:
        db.add_subcategory(
            cat_id,
            product_name,
            product_cost,
            product_url,
            product_type,
            message.photo[-1].file_id
        )
    else:
        db.add_subcategory(
            cat_id,
            product_name,
            product_cost,
            product_url,
            product_type
        )

    await User.admin.start.set()
    await message.answer(
        text=f'Товар {product_name} добавлен!',
        reply_markup=Keyboards.admin_menu()
    )


async def choice_product(call: types.CallbackQuery):
    user_id = call.from_user.id
    temp = call.data.split('|')

    if temp[1] == 'next':
        await bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=call.message.message_id,
            reply_markup=Keyboards.adm_products(int(temp[2]))
        )

    elif temp[1] == 'back':
        await bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=call.message.message_id,
            reply_markup=Keyboards.adm_products(int(temp[2]))
        )

    elif temp[1] == 'menu':
        await User.admin.start.set()
        await bot.edit_message_text(
            chat_id=user_id,
            text='Админ меню',
            message_id=call.message.message_id,
            reply_markup=Keyboards.admin_menu()
        )

    else:
        await bot.edit_message_text(
            chat_id=user_id,
            text='Выберите настройку:',
            message_id=call.message.message_id,
            reply_markup=Keyboards.change_sub(temp[1], temp[2])
        )


async def change_sub(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    temp = call.data.split('|')

    if temp[1] == 'del':
        db.delete_subcategory(temp[2], temp[3])

        await User.admin.change_sub.set()
        await bot.edit_message_text(
            chat_id=user_id,
            text='Выберите нужный товар:',
            message_id=call.message.message_id,
            reply_markup=Keyboards.adm_products(0)
        )

    if temp[1] == 'cost':
        await call.answer()

        async with state.proxy() as data:
            data['cat_id'] = temp[2]
            data['sub_id'] = temp[3]

        await bot.send_message(
            chat_id=user_id,
            text='Введите новую цену товара'
        )

    if temp[1] == 'sub_name':
        await call.answer()

        async with state.proxy() as data:
            data['cat_id'] = temp[2]
            data['sub_id'] = temp[3]

        await User.admin.change_sub_name.set()
        await bot.send_message(
            chat_id=user_id,
            text='Введите новое название товара'
        )

    if temp[1] == 'back':
        await User.admin.change_sub.set()
        await bot.edit_message_text(
            chat_id=user_id,
            text='Выберите нужный товар:',
            message_id=call.message.message_id,
            reply_markup=Keyboards.adm_products(0)
        )


async def update_cost_sub(message: types.Message, state: FSMContext):
    try:
        r = float(message.text) + 0.5

    except ValueError:
        await message.answer(
            text='Неверное значение!'
        )
        return

    async with state.proxy() as data:
        cat_id = data['cat_id']
        sub_id = data['sub_id']

    db.update_cost_product(cat_id, sub_id, int(message.text))

    await User.admin.change_sub.set()
    await message.answer(
        text='Значение изменено!',
        reply_markup=Keyboards.adm_products(0)
    )


async def update_sub_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        cat_id = data['cat_id']
        sub_id = data['sub_id']

    db.update_product_name(cat_id, sub_id, message.text)

    await User.admin.change_sub.set()
    await message.answer(
        text='Значение изменено!',
        reply_markup=Keyboards.adm_products(0)
    )


#########################
async def choice_sub_product(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    temp = call.data.split('|')

    if temp[1] == 'next':
        await bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=call.message.message_id,
            reply_markup=Keyboards.adm_products(int(temp[2]))
        )

    elif temp[1] == 'back':
        await bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=call.message.message_id,
            reply_markup=Keyboards.adm_products(int(temp[2]))
        )

    elif temp[1] == 'menu':
        await User.admin.start.set()
        await bot.edit_message_text(
            chat_id=user_id,
            text='Админ меню',
            message_id=call.message.message_id,
            reply_markup=Keyboards.admin_menu()
        )
    else:
        await call.answer()

        async with state.proxy() as data:
            data['cat_id'] = temp[1]
            data['sub_id'] = temp[2]

        await bot.send_message(
            chat_id=user_id,
            text='Отправьте txt файл с товарами построчно.\n\n'
                 'товар\n'
                 'товар\n'
                 'товар\n\n'
                 'Если товар выдается администратором, просто укажите доступное количество товара числом.\n\n'
                 '100'
        )


async def get_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        cat_id = data['cat_id']
        sub_id = data['sub_id']

    if message.document:
        file_name = f'./{message.document.file_name}'

        get = await bot.get_file(message.document.file_id)
        await bot.download_file(get.file_path, file_name)

        with open(file_name, 'r') as file:
            r = list(set([i.strip() for i in file if not db.product_exists(i.strip())]))

        os.remove(file_name)

        for i in r:
            db.add_product(cat_id, sub_id, i)

        await User.admin.start.set()
        await message.answer(
            text=f'✅ Добавлено {len(r)} новых товаров!',
            reply_markup=Keyboards.admin_menu()
        )

    else:
        db.add_product(cat_id, sub_id, int(message.text))

        await User.admin.start.set()
        await message.answer(
            text=f'✅ Добавлено {int(message.text)} новых товаров!',
            reply_markup=Keyboards.admin_menu()
        )


async def mail_text(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    try:
        r = await message.answer(message.text)
        await bot.delete_message(user_id, r.message_id)

    except aiogram.exceptions.CantParseEntities:
        await message.answer('Неверное заполнение HTML')
        return

    async with state.proxy() as data:
        data['text'] = message.text

    await User.admin.mail_photo.set()
    await bot.send_message(
        chat_id=user_id,
        text='Если хотите добавить фото, отправьте его, если нет - отправьте любой символ.'
    )


async def mail_photo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if message.photo:
        async with state.proxy() as data:
            data['photo'] = message.photo[-1].file_id
            caption = data['text']

        await bot.send_photo(
            chat_id=user_id,
            photo=message.photo[-1].file_id,
            caption=caption,
            reply_markup=Keyboards.accept_mail()
        )

    if message.text:
        async with state.proxy() as data:
            data['photo'] = None
            text = data['text']

        await bot.send_message(
            chat_id=user_id,
            text=text,
            reply_markup=Keyboards.accept_mail()
        )


async def accept_mail(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    temp = call.data.split('|')

    if temp[1] == 'y':
        async with state.proxy() as data:
            photo = data['photo']
            text = data['text']

        count_a = 0
        count_r = 0

        for i in db.get_users()[3]:
            try:
                if not photo:
                    await bot.edit_message_text(
                        chat_id=user_id,
                        text='<b>Рассылка запущена:</b>\n\n'
                             f'Прогресс: {count_a + count_r} / {len(db.get_users()[3])}\n'
                             f'Отправлено: {count_a}\n'
                             f'Ошибок: {count_r}',
                        message_id=call.message.message_id
                    )

                    await bot.send_message(
                        chat_id=i[1],
                        text=text
                    )
                else:
                    await bot.edit_message_caption(
                        chat_id=user_id,
                        caption='<b>Рассылка запущена:</b>\n\n'
                                f'Прогресс: {count_a + count_r} / {len(db.get_users()[3])}\n'
                                f'Отправлено: {count_a}\n'
                                f'Ошибок: {count_r}',
                        message_id=call.message.message_id
                    )

                    await bot.send_photo(
                        chat_id=i[1],
                        photo=photo,
                        caption=text
                    )
                count_a += 1
                await asyncio.sleep(0.25)

            except aiogram.exceptions.BotBlocked:
                count_r += 1
                db.delete_user(i[1])
                await asyncio.sleep(0.25)
                continue

            except aiogram.exceptions.UserDeactivated:
                count_r += 1
                db.delete_user(i[1])
                await asyncio.sleep(0.25)
                continue

            except Exception as e:
                print(e)
                db.delete_user(i[1])
                await asyncio.sleep(0.25)
                continue

        await bot.delete_message(user_id, call.message.message_id)

        await User.admin.start.set()
        await bot.send_message(
            chat_id=user_id,
            text='<b>Рассылка окончена:</b>\n\n'
                 f'Прогресс: {count_a + count_r} / {len(db.get_users()[3])}\n'
                 f'Отправлено: {count_a}\n'
                 f'Ошибок: {count_r}',
            reply_markup=Keyboards.admin_menu()
        )

    if temp[1] == 'n':
        await bot.delete_message(user_id, call.message.message_id)

        await User.admin.start.set()
        await bot.send_message(
            chat_id=user_id,
            text=f'<b>Админ меню</b>\n\n'
                 f'Пользователи:\n'
                 f'День: {db.get_users()[0]}\n'
                 f'Неделя: {db.get_users()[1]}\n'
                 f'Месяц: {db.get_users()[2]}\n'
                 f'Всего: {len(db.get_users()[3])}',
            reply_markup=Keyboards.admin_menu()
        )


def fhand_add(dp: Dispatcher):
    dp.register_message_handler(admin, commands=['adm', 'balance'], state='*')

    dp.register_message_handler(get_category_name, content_types=['text'], state=User.admin.add_cat)
    dp.register_message_handler(get_category_photo, content_types=['text', 'photo'], state=User.admin.add_cat_photo)

    dp.register_callback_query_handler(choice_category, lambda c: c.data and c.data.startswith('g'),
                                       state=User.admin.add_sub)
    dp.register_message_handler(get_product_info, content_types=['text'], state=User.admin.add_sub)
    dp.register_message_handler(get_product_photo, content_types=['text', 'photo'], state=User.admin.add_sub_photo)

    dp.register_callback_query_handler(choice_cat, lambda c: c.data and c.data.startswith('g'),
                                       state=User.admin.change_cat)
    dp.register_callback_query_handler(change_cat, lambda c: c.data and c.data.startswith('k'),
                                       state=User.admin.change_cat)
    dp.register_message_handler(update_cat_name, content_types=['text'], state=User.admin.change_cat_name)

    dp.register_callback_query_handler(choice_product, lambda c: c.data and c.data.startswith('g'),
                                       state=User.admin.change_sub)
    dp.register_callback_query_handler(change_sub, lambda c: c.data and c.data.startswith('h'),
                                       state=User.admin.change_sub)

    dp.register_message_handler(update_cost_sub, content_types=['text'], state=User.admin.change_sub)
    dp.register_message_handler(update_sub_name, content_types=['text'], state=User.admin.change_sub_name)

    dp.register_callback_query_handler(choice_sub_product, lambda c: c.data and c.data.startswith('g'),
                                       state=User.admin.add_product)
    dp.register_message_handler(get_product, content_types=['text', 'document'], state=User.admin.add_product)

    dp.register_callback_query_handler(choice, lambda c: c.data and c.data.startswith('admin'),
                                       state=User.admin.start)

    dp.register_message_handler(mail_text, content_types=['text'], state=User.admin.mail_text)
    dp.register_message_handler(mail_photo, content_types=['text', 'photo'], state=User.admin.mail_photo)
    dp.register_callback_query_handler(accept_mail, lambda c: c.data and c.data.startswith('admin'),
                                       state=User.admin.mail_photo)
