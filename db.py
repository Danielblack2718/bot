import random
import sqlite3


class Database:
    def __init__(self):
        self.connect = sqlite3.connect('db.db')

    def execute(self, sql, *args):
        with self.connect as database:
            cursor = database.cursor()
            cursor.execute(sql, *args)
            database.commit()

    def fetchone(self, sql, *args):
        with self.connect as database:
            cursor = database.cursor()
            res = cursor.execute(sql, *args)
            return res.fetchone()

    def fetchall(self, sql, *args):
        with self.connect as database:
            cursor = database.cursor()
            res = cursor.execute(sql, *args)
            return res.fetchall()

    @staticmethod
    def format_args(*args):
        formatting = [i for i in args]
        return tuple(formatting)

    def create_tables(self):
        self.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        date DATE,
                        geo TEXT,
                        currency TEXT)
                        ''')
        print('Юзеры запущены')

        self.execute('''CREATE TABLE IF NOT EXISTS category (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cat_id INTEGER,
                        cat_name TEXT,
                        cat_photo TEXT)
                        ''')
        print('Категории запущены')

        self.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cat_id INTEGER,
                        product_id INTEGER,
                        product_name TEXT,
                        product_cost INTEGER,
                        product_photo TEXT,
                        product_url TEXT,
                        product_type INTEGER)
                        ''')
        print('Товары запущены')

        self.execute('''CREATE TABLE IF NOT EXISTS remains (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cat_id INTEGER,
                        product_id INTEGER,
                        body TEXT)
                        ''')
        print('Остаток товаров')

        self.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        order_id INTEGER,
                        product_name TEXT,
                        user_id INTEGER,
                        order_cost INTEGER,
                        order_date DATE)
                        ''')
        print('История покупок запущена')

    def get_user_history_orders(self, user_id):
        sql = 'SELECT * FROM orders WHERE user_id = ?'

        payments = self.fetchall(sql, db.format_args(user_id))

        return '\n'.join([f'<b>{a + 1}. {i[1]} | {i[2]} | {i[4]} | {i[5]}</b>'
                          for a, i in enumerate(payments) if a < 9])

    '''Запросы касающиеся юзеров'''
    def user_exists(self, user_id):
        sql = 'SELECT user_id FROM users WHERE user_id = ?'

        if not self.fetchone(sql, db.format_args(user_id)):
            return False

        return True

    def add_user(self, user_id, date, geo):
        sql = 'INSERT INTO users (user_id, date, geo, currency) VALUES (?, ?, ?, ?)'
        self.execute(sql, db.format_args(user_id, date, geo, 'RUB'))

    def get_info_user(self, user_id):
        sql = 'SELECT * FROM users WHERE user_id = ?'
        return self.fetchone(sql, db.format_args(user_id))

    def update_balance(self, user_id, amount, func):
        if func == 'add':
            sql = f'UPDATE users SET balance = balance + {amount} WHERE user_id = ?'
            self.execute(sql, db.format_args(user_id))
        if func == 'del':
            sql = f'UPDATE users SET balance = balance - {amount} WHERE user_id = ?'
            self.execute(sql, db.format_args(user_id))

    def update_lang(self, user_id, lang):
        sql = 'UPDATE users SET geo = ? WHERE user_id = ?'
        self.execute(sql, db.format_args(lang, user_id))

    def update_currency(self, user_id, currency):
        sql = 'UPDATE users SET currency = ? WHERE user_id = ?'
        self.execute(sql, db.format_args(currency, user_id))

    def delete_user(self, user_id):
        sql = 'DELETE FROM users WHERE user_id = ?'
        self.execute(sql, db.format_args(user_id))

    def add_payment(self, user_id, payment_date, amount, t_id, method=None):
        sql = 'INSERT INTO history_payment (user_id, payment_date, amount, method, hash) VALUES (?, ?, ?, ?, ?)'
        self.execute(sql, db.format_args(user_id, payment_date, amount, method, t_id))

    def payment_exists(self, t_id):
        sql = 'SELECT hash FROM history_payment WHERE hash = ?'

        if not self.fetchone(sql, db.format_args(t_id)):
            return False

        return True

    def get_user_payment(self, user_id):
        sql = 'SELECT amount FROM history_payment WHERE user_id = ?'
        return sum([int(i[0]) for i in self.fetchall(sql, db.format_args(user_id))])

    def get_all_payment(self):
        day = '''SELECT amount 
                 FROM history_payment 
                 WHERE payment_date = strftime("%Y-%m-%d", "now")
                 AND method != "promo"
                 '''
        summ_day = 0
        for i in self.fetchall(day):
            summ_day += i[0]

        week = '''SELECT amount 
                  FROM history_payment 
                  WHERE payment_date
                  BETWEEN strftime("%Y-%m-%d", "now", "-7 days") 
                  AND strftime("%Y-%m-%d", "now", "+7 days")
                  AND method != "promo"
                  '''
        summ_week = 0
        for i in self.fetchall(week):
            summ_week += i[0]

        month = '''SELECT amount 
                   FROM history_payment 
                   WHERE payment_date
                   BETWEEN strftime("%Y-%m-%d", "now", "-30 days") 
                   AND strftime("%Y-%m-%d", "now", "+30 days")
                   AND method != "promo"
                   '''
        summ_month = 0
        for i in self.fetchall(month):
            summ_month += i[0]

        all_stat = '''SELECT amount FROM history_payment WHERE method != "promo"'''
        summ_all_stat = 0
        for i in self.fetchall(all_stat):
            summ_all_stat += i[0]

        return round(summ_day, 2), round(summ_week, 2), round(summ_month, 2), round(summ_all_stat, 2)

    def get_order_user(self, user_id):
        sql = 'SELECT * FROM orders WHERE user_id = ?'
        return len(self.fetchall(sql, db.format_args(user_id)))

    def add_order(self, order_id, user_id, order_cost, order_date, product_name):
        sql = 'INSERT INTO orders (order_id, user_id, order_cost, order_date, product_name) VALUES (?, ?, ?, ?, ?)'
        self.execute(sql, db.format_args(order_id, user_id, order_cost, order_date, product_name))

    def get_all_orders(self):
        sql = 'SELECT * FROM orders'
        return len(self.fetchall(sql))

    def add_category(self, name, photo):
        cat_id = ''.join([str(random.randint(1, 9)) for _ in range(10)])
        sql = 'INSERT INTO category (cat_id, cat_name, cat_photo) VALUES (?, ?, ?)'
        self.execute(sql, db.format_args(cat_id, name, photo))

    def delete_category(self, cat_id):
        sql = 'DELETE FROM category WHERE cat_id = ?'
        self.execute(sql, db.format_args(cat_id))

    def update_cat_name(self, cat_id, cat_name):
        sql = 'UPDATE category SET cat_name = ? WHERE cat_id = ?'
        self.execute(sql, db.format_args(cat_name, cat_id))

    def get_info_category(self, cat_id):
        sql = 'SELECT * FROM category WHERE cat_id = ?'
        return self.fetchone(sql, db.format_args(cat_id))

    def get_all_category(self):
        sql = 'SELECT * FROM category'
        return self.fetchall(sql)

    def add_subcategory(self, cat_id, product_name, product_cost, product_url, product_type, product_photo='0'):
        product_id = ''.join([str(random.randint(1, 9)) for _ in range(10)])
        sql = '''INSERT INTO products 
                 (cat_id, product_id, product_name, product_cost, product_photo, product_url, product_type) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)'''
        self.execute(
            sql,
            db.format_args(cat_id, product_id, product_name, product_cost, product_photo, product_url, product_type)
        )

    def delete_subcategory(self, cat_id, sub_id):
        sql = 'DELETE FROM products WHERE cat_id = ? AND product_id = ?'
        self.execute(sql, db.format_args(cat_id, sub_id))

    def update_cost_product(self, cat_id, product_id, amount):
        sql = 'UPDATE products SET product_cost = ? WHERE cat_id = ? AND product_id = ?'
        self.execute(sql, db.format_args(amount, cat_id, product_id))

    def update_product_name(self, cat_id, product_id, sub_name):
        sql = 'UPDATE products SET product_name = ? WHERE cat_id = ? AND product_id = ?'
        self.execute(sql, db.format_args(sub_name, cat_id, product_id))

    def get_subcategory(self, cat_id):
        sql = 'SELECT * FROM subcategory WHERE cat_id = ?'
        return self.fetchall(sql, db.format_args(cat_id))

    def get_info_subcategory(self, sub_id):
        sql = 'SELECT * FROM subcategory WHERE sub_id = ?'
        return self.fetchone(sql, db.format_args(sub_id))

    def get_all_products(self):
        sql = 'SELECT * FROM products'
        return self.fetchall(sql)

    def get_products(self, cat_id):
        sql = 'SELECT * FROM products WHERE cat_id = ?'
        return self.fetchall(sql, db.format_args(cat_id))

    def get_remain_product(self, cat_id, product_id, adm_product=None):
        if not adm_product:
            sql = 'SELECT * FROM remains WHERE cat_id = ? AND product_id = ?'
            return self.fetchall(sql, db.format_args(cat_id, product_id))

        else:
            sql = 'SELECT body FROM remains WHERE cat_id = ? AND product_id = ?'
            try:
                return self.fetchone(sql, db.format_args(cat_id, product_id))[0]

            except TypeError:
                return 0

    def product_exists(self, body):
        sql = 'SELECT body FROM remains WHERE body = ?'

        if not self.fetchone(sql, db.format_args(body)):
            return False

        return True

    def get_info_product(self, product_id):
        sql = 'SELECT * FROM products WHERE product_id = ?'
        return self.fetchone(sql, db.format_args(product_id))

    def add_product(self, cat_id, sub_id, body):

        sql = 'INSERT INTO remains (cat_id, product_id, body) VALUES (?, ?, ?)'

        if not isinstance(body, int):
            self.execute(sql, db.format_args(cat_id, sub_id, body))

        else:
            sql2 = 'SELECT body FROM remains WHERE cat_id = ? AND product_id = ?'

            if not self.fetchone(sql2, db.format_args(cat_id, sub_id)):
                self.execute(sql, db.format_args(cat_id, sub_id, body))

            else:
                sql = 'UPDATE remains SET body = ? WHERE cat_id = ? AND product_id = ?'
                self.execute(sql, db.format_args(body, cat_id, sub_id))

    def delete_remains(self, body=None, cat_id=None, product_id=None, count=None):

        if body:
            sql = 'DELETE FROM remains WHERE body = ?'
            self.execute(sql, db.format_args(body))

        else:
            sql = 'UPDATE remains SET body = body - ? WHERE cat_id = ? AND product_id = ?'
            self.execute(sql, db.format_args(count, cat_id, product_id))

    def get_users(self):
        day = '''SELECT user_id
                 FROM users
                 WHERE date = strftime("%Y-%m-%d", "now")
                 '''
        day = self.fetchall(day)

        week = '''SELECT user_id
                  FROM users
                  WHERE date
                  BETWEEN strftime("%Y-%m-%d", "now", "-7 days") 
                  AND strftime("%Y-%m-%d", "now", "+7 days")
                  '''
        week = self.fetchall(week)

        month = '''SELECT user_id
                   FROM users
                   WHERE date
                   BETWEEN strftime("%Y-%m-%d", "now", "-30 days") 
                   AND strftime("%Y-%m-%d", "now", "+30 days")
                   '''
        month = self.fetchall(month)

        all_users = 'SELECT * FROM users'

        return len(day), len(week), len(month), self.fetchall(all_users)


db = Database()
