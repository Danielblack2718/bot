from aiogram.dispatcher.filters.state import State, StatesGroup


class menu(StatesGroup):
    start = State()
    support = State()
    count_pay = State()


class dob(StatesGroup):
    start = State()


class buy(StatesGroup):
    start = State()
    check = State()


class admin(StatesGroup):
    start = State()
    mail_text = State()
    mail_photo = State()
    setting = State()

    add_cat = State()
    add_cat_photo = State()
    change_cat = State()
    change_cat_name = State()

    add_sub = State()
    add_sub_photo = State()
    change_sub = State()
    change_sub_name = State()

    add_product = State()

    change_ref = State()
    change_address = State()

    add_discount = State()
