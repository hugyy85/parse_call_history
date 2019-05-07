import config, peewee, glob, re
import pymysql
import models
from bs4 import BeautifulSoup


def create_database(charset="utf8mb4"):

    cursor_type = pymysql.cursors.DictCursor
    connection_instance = pymysql.connect(
        host=config.server_IP,
        user=config.user_name,
        password=config.user_password,
        charset=charset,
        cursorclass=cursor_type
    )

    try:
        # Create a cursor object
        cursor_instance = connection_instance.cursor()
        # SQL Statement to create a database
        sql_statement = "CREATE DATABASE " + config.database_name
        # Execute the create database SQL statement through the cursor instance
        cursor_instance.execute(sql_statement)

    except Exception as e:
        print("Exception occured:{}".format(e))

    finally:
        connection_instance.close()


def _save_row(row):
    try:
        row.save()
    except peewee.InternalError as px:
        print(str(px))
    except peewee.IntegrityError as px:
        print(str(px))


def add_row_to_user(num, date, time, number, how_long):
    row = models.User(
        whois=num,
        date=date,
        time=time,
        number=number,
        how_long=how_long,
    )
    _save_row(row)


def add_rows_to_names():
    with open('Номера телефонов - фамилии агентов.txt', 'r') as f:
        text = f.read()

    text = text.split('\n')
    for i in text:
        i = i.split(' ')
        row = models.Names(
            whois=i[0],
            name=i[1],
        )
        _save_row(row)


def add_user_name(num, name):
    row = models.User(
        whois=num,
        name=name,
    )
    _save_row(row)


def connection():
    try:
        models.dbhandle.close()
    except:
        pass
    models.dbhandle.connect()


def create_tables():

    try:
        connection()
        models.User.create_table()

    except peewee.InternalError as px:
        print(str(px))

    try:
        models.Names.create_table()
    except peewee.InternalError as px:
        print(str(px))


def parse_phones():
    for file in glob.glob('*.html'):
        with open(file, encoding='utf-8') as f:
            html = f.read()
        num = re.findall(r'7\d{10}', file)
        soup = BeautifulSoup(html, 'lxml')
        for row in soup.tbody:
            a = row.contents
            add_row_to_user(num[0], a[1].next, a[2].next, a[4].next, a[9].next)

    return num[0]


