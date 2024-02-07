import math
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
import Config
from db import db


def channel():
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton(
            text='🔗 Подписаться',
            url=Config.admin_channel_url
        )
    )
    kb.add(
        InlineKeyboardButton(
            text='✅ Проверить',
            callback_data='6sub'
        )
    )

    return kb


def lan():
    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton(
            text='Русский 🇷🇺',
            callback_data='lang|ru'
        ),
        InlineKeyboardButton(
            text='English 🇺🇸',
            callback_data='lang|en'
        )
    )

    return kb


def menu(lang=None):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    kb.add(
        '🛍 Товары 🛍',
        '👤 Профиль 👤',
        '📝 Отзывы 📝',
        '☎ Поддержка ☎',
        '❓ FAQ ❓'
    )

    return kb


def category(remover, adm=None):
    kb = InlineKeyboardMarkup(row_width=3)

    tag = 'r'
    if adm:
        tag = 'g'

    cat = db.get_all_category()

    for a, i in enumerate(range(remover, len(cat))):
        if a < 10:
            kb.add(
                InlineKeyboardButton(
                    text=cat[i][2],
                    callback_data=f'{tag}|{cat[i][1]}'
                )
            )

    if len(cat) <= 10:
        pass

    elif len(cat) > 10 > remover:
        kb.add(InlineKeyboardButton(text='➡️', callback_data=f'{tag}|next|{remover + 10}'))

    elif remover + 10 >= len(cat):
        kb.add(InlineKeyboardButton(text='⬅️', callback_data=f'{tag}|back|{remover - 10}'))

    else:
        kb.add(InlineKeyboardButton(text='⬅️', callback_data=f'{tag}|back|{remover - 10}'),
               InlineKeyboardButton(text=f'{str(remover + 10)[:-1]}/{math.ceil(len(cat) / 10)}',
                                    callback_data='...'),
               InlineKeyboardButton(text='➡️', callback_data=f'{tag}|next|{remover + 10}'))

    if adm:
        kb.add(
            InlineKeyboardButton(
                text='Вернуться',
                callback_data=f'{tag}|menu'
            )
        )

    return kb


def products(cat_id, remover, currency='RUB', lang=None, usd_to_rub=None):
    kb = InlineKeyboardMarkup(row_width=1)

    get_products = db.get_products(cat_id)

    for a, i in enumerate(range(remover, len(get_products))):
        if a < 10:
            if currency == 'RUB':
                price = get_products[i][4]

            else:
                price = int(get_products[i][4] / usd_to_rub)

            kb.add(
                InlineKeyboardButton(
                    text=f'{get_products[i][3]} | {price} {currency}',
                    callback_data=f's|{get_products[i][1]}|{get_products[i][2]}|{price}'
                )
            )

    if len(get_products) <= 10:
        pass

    elif len(get_products) > 10 > remover:
        kb.add(InlineKeyboardButton(text='➡️', callback_data=f's|next|{remover + 10}|{cat_id}'))

    elif remover + 10 >= len(get_products):
        kb.add(InlineKeyboardButton(text='⬅️', callback_data=f's|back|{remover - 10}|{cat_id}'))

    else:
        kb.add(InlineKeyboardButton(text='⬅️', callback_data=f's|back|{remover - 10}|{cat_id}'),
               InlineKeyboardButton(text=f'{str(remover + 10)[:-1]}/{math.ceil(len(get_products) / 10)}',
                                    callback_data='...'),
               InlineKeyboardButton(text='➡️', callback_data=f's|next|{remover + 10}|{cat_id}'))

    kb.add(
        InlineKeyboardButton(
            text='Вернуться',
            callback_data=f's|menu'
        )
    )

    return kb


def adm_products(remover):
    kb = InlineKeyboardMarkup(row_width=1)

    all_products = db.get_all_products()

    for a, i in enumerate(range(remover, len(all_products))):
        if a < 10:
            cat = db.get_info_category(all_products[a][1])

            kb.add(
                InlineKeyboardButton(
                    text=f'{cat[2]} / {all_products[a][3]}',
                    callback_data=f'g|{all_products[a][1]}|{all_products[a][2]}'
                )
            )

    if len(all_products) <= 10:
        pass

    elif len(all_products) > 10 > remover:
        kb.add(InlineKeyboardButton(text='➡️', callback_data=f'g|next|{remover + 10}'))

    elif remover + 10 >= len(all_products):
        kb.add(InlineKeyboardButton(text='⬅️', callback_data=f'g|back|{remover - 10}'))

    else:
        kb.add(InlineKeyboardButton(text='⬅️', callback_data=f'g|back|{remover - 10}'),
               InlineKeyboardButton(text=f'{str(remover + 10)[:-1]}/{math.ceil(len(all_products) / 10)}',
                                    callback_data='...'),
               InlineKeyboardButton(text='➡️', callback_data=f'g|next|{remover + 10}'))

    kb.add(
        InlineKeyboardButton(
            text='Вернуться',
            callback_data=f'g|menu'
        )
    )

    return kb


def actions_product(cat_id, product_id, price, lang=None):
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton(
            text='💸 Купить товар',
            callback_data=f'b|buy|{cat_id}|{product_id}|{price}'
        ),
        InlineKeyboardButton(
            text='Вернуться',
            callback_data=f'b|back|{cat_id}'
        )
    )

    return kb


def accept_buy(count, amount, cat_id, product_id, lang=None):
    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton(
            text='✅ Да, купить',
            callback_data=f'c|y|{count}|{amount}|{cat_id}|{product_id}'
        ),
        InlineKeyboardButton(
            text='❌ Нет, отменить',
            callback_data=f'c|n'
        )
    )

    return kb


def choice_payment():
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton(
            text='AAIO',
            callback_data='y|aaio'
        )
    )

    return kb


def check_payment(pay_url, order_id, lang=None):
    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton(
            text='💸 Перейти к оплате',
            url=pay_url
        )
    )
    kb.add(
        InlineKeyboardButton(
            text='♻️ Проверить оплату',
            callback_data=f'check|{order_id}'
        ),
        InlineKeyboardButton(
            text='🚫 Отменить',
            callback_data='check|cancel'
        )
    )

    return kb


def profile(lang=None):
    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton(
            text='🛒 История покупок',
            callback_data='3history'
        )
    )
    kb.add(
        InlineKeyboardButton(
            text='🚩 Изменить язык',
            callback_data='1language'
        ),
        InlineKeyboardButton(
            text='💱 Изменить валюту',
            callback_data='2currency'
        )
    )

    return kb


def reviews():
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton(
            text='Ссылка на темы',
            url='1.com'
        )
    )

    return kb


def support(lang=None):
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton(
            text='💌 Написать в поддержку',
            url='1.com'
        )
    )

    return kb


def faq():
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton(
            text='FAQ 🧐',
            url='1.com'
        )
    )

    return kb


def back(lang=None):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add(
        'Вернуться назад'
    )

    return kb


def admin_menu():
    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton(
            text='📩 Рассылка',
            callback_data='admin|mail'
        )
    )
    kb.add(
        InlineKeyboardButton(
            text='Добавить категорию',
            callback_data='admin|category'
        ),
        InlineKeyboardButton(
            text='Изменить категорию',
            callback_data='admin|change_cat'
        ),
        InlineKeyboardButton(
            text='Добавить товар',
            callback_data='admin|product'
        ),
        InlineKeyboardButton(
            text='Изменить товар',
            callback_data='admin|change_product'
        ),
        InlineKeyboardButton(
            text=f'Залить товары',
            callback_data='admin|add_products'
        )
    )

    return kb


def change_cat(cat_id):
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton(
            text='Изменить название',
            callback_data=f'k|cat_name|{cat_id}'
        ),
        InlineKeyboardButton(
            text='Удалить',
            callback_data=f'k|del|{cat_id}'
        ),
        InlineKeyboardButton(
            text='Вернуться',
            callback_data='k|back'
        )
    )

    return kb


def change_sub(cat_id, sub_id):
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton(
            text='Удалить',
            callback_data=f'h|del|{cat_id}|{sub_id}'
        ),
        InlineKeyboardButton(
            text='Изменить цену',
            callback_data=f'h|cost|{cat_id}|{sub_id}'
        ),
        InlineKeyboardButton(
            text='Изменить название',
            callback_data=f'h|sub_name|{cat_id}|{sub_id}'
        ),
        InlineKeyboardButton(
            text='Вернуться',
            callback_data='h|back'
        )
    )

    return kb


def accept_delete_products(cat_id, sub_id):
    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton(
            text='✅ Да',
            callback_data=f'a|y|{cat_id}|{sub_id}'
        ),
        InlineKeyboardButton(
            text='❌ Нет',
            callback_data=f'a|n'
        )
    )

    return kb


def accept_mail():
    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton(
            text='📩 Запустить',
            callback_data='admin|y'
        ),
        InlineKeyboardButton(
            text='❌ Отменить',
            callback_data='admin|n'
        )
    )

    return kb
