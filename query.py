from models import *
import config, peewee


def how_long_month(whois, number=None):
    try:
        query2 = Names.select().where(Names.whois == whois).get()
        name = query2.name
    except peewee.ProgrammingError as px:
        if px.args[0] == 1146:
            print('Добавьте данные о номере в файл "Номера телефонов - фамилии агентов.txt"')
        name = whois

    if number:
        query = User.select().where(((User.number == number) | (User.number == f'<--{number}')) & (User.whois == whois))
    elif not number:
        query = User.select().where(User.whois == whois)

    time_result = 0
    internet = 0
    for i in query:
        long = i.how_long.split(':')
        t = i.time.split(':')

        if config.at < int(t[0]) < config.to:  # время рабочее с 7 до 18
            try:
                time_result += (int(long[0]) * 60) + int(long[1])
            except IndexError:
                pass
            except ValueError:
                internet += int(i.how_long.split('Kb')[0])

    return name, round(time_result/3600, 2), round(internet/1024, 2)


def sort_dictionary_by_value(dictionary):
    list_of_sorted_pairs = [(k, dictionary[k]) for k in sorted(dictionary.keys(), key=dictionary.get, reverse=False)]

    return list_of_sorted_pairs


def write_result(dict1, dict2):
    dict1 = sort_dictionary_by_value(dict1)
    dict2 = sort_dictionary_by_value(dict2)

    with open('Результаты.txt', 'w') as f:
        f.write('Разговоры: \n')
        for i in reversed(dict1):
            f.write(f'{i[0]} {i[1]} часа телефонных разговоров в рабочее время\n')

        f.write('Интернет: \n')
        for i in reversed(dict2):
            f.write(f'{i[0]} {i[1]}Mb траффика в рабочее время\n')


def lider():
    query = User.select().group_by(User.whois)
    phone = {}
    internet = {}
    for i in query:
        num = how_long_month(i.whois)
        phone[num[0]] = num[1]
        internet[num[0]] = num[2]

    write_result(phone, internet)


def rating_numbers():
    query = User.select().group_by(User.number)
    query2 = User.select().group_by(User.whois).get()
    phone = {}
    internet = {}

    for i in query:
        if i.number[0:3] == '<--':
            continue
        elif i.number.isdigit():
            num = how_long_month(query2.whois, i.number)
            phone[i.number] = num[1]
        else:
            num = how_long_month(query2.whois, i.number)
            internet[i.number] = num[2]

    write_result(phone, internet)
