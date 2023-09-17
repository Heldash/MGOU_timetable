# # -*- coding: UTF-8 -*-
import datetime
import os
import time
import telebot
from telebot import types

import parsing_mgou
import datetime as dt
import json
import re
from GoogleShetrob import update
from update_raspV2 import upload_rasp
# from raspisanie_update import upload_rasp
import TOKEN
from threading import Thread
import schedule

token1_osnov = TOKEN.TOKEN
token2 = TOKEN.TOKEN1
bot = telebot.TeleBot(TOKEN.TOKEN1, parse_mode="HTML")

stikers_list = ["CAACAgQAAxkBAAEGn9Bjh0tp3dzMwK5JO1BvSVI0yCUsAQACOw0AAtbmSFAxK-1eG55cfCsE",
                "CAACAgEAAxkBAAEGn9Rjh0z1rnIVn85ZVPXa9DZBUnkFLgACawQAAvhi8ERmUaTo2t1t_ysE",
                "CAACAgIAAxkBAAEGn9Zjh01Aw8ick5OeDUs06WTWJYcdQAACXAEAAhAabSKcIs6F61GChSsE",
                "CAACAgQAAxkBAAEGn9hjh04AAXlITxIq_Jaz10xVdTlyuH4AAkMLAALo4aBSIDcpNsGm758rBA",
                "CAACAgIAAxkBAAEGomVjiHEw3k0rKIbKRjjtmCYg06xAhQAC0RsAAhyGcUjQ7Rs7CfNrAysE",
                "CAACAgEAAxkBAAEGomdjiHSYhtzKYOODjoS-_0l60dh74QACnAIAAtscqEdAo37j6Iyu8CsE"]

abrev = {'Факультет безопасности жизнедеятельности': 'OBZ',
         'Факультет естественных наук': 'SIEN',
         'Факультет изобразительного искусства и народных ремёсел': 'IMAG',
         'Факультет истории, политологии и права': 'HPP',
         'Лингвистический факультет': 'LINGV',
         'Факультет психологии': 'PSYH',
         'Факультет романо-германских языков': 'RGLANG',
         'Факультет русской филологии': 'RFIL',
         'Факультет специальной педагогики и психологии': 'SOCPED',
         'Физико-математический факультет': 'PHYS',
         'Факультет физической культуры': 'FIZK',
         'Экономический факультет': 'ECONOM',
         'Юридический факультет': 'YRID',
         'Медицинский факультет': 'MED',
         }  # Факултеты и их сокращения
abrev_rash = {'OBZ': 'Факультет безопасности жизнедеятельности',
              'SIEN': 'Факультет естественных наук',
              'IMAG': 'Факультет изобразительного искусства и народных ремёсел',
              'HPP': 'Факультет истории, политологии и права',
              'LINGV': 'Лингвистический факультет',
              'PSYH': 'Факультет психологии',
              'RGLANG': 'Факультет романо-германских языков',
              'RFIL': 'Факультет русской филологии',
              'SOCPED': 'Факультет специальной педагогики и психологии',
              'PHYS': 'Физико-математический факультет',
              'FIZK': 'Факультет физической культуры',
              'ECONOM': 'Экономический факультет',
              'YRID': 'Юридический факультет',
              'MED': 'Медицинский факультет', }  # Расшифровка абревиатур

users = {}
activ_us = []
req = 0


def open_users_data(user_id: str) -> list:
    with open("Users.json", "r") as file:
        user_id = str(user_id)
        try:
            us = json.load(file)  # словарь со списком всех пользователей
        except:
            us = None
        if us is not None:
            if user_id in us:
                return us[user_id]
            elif user_id not in us:
                return None
        else:
            return None


month = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь",
         "Ноябрь", "Декабрь"]
wday = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
stickers_arr = ["CAACAgQAAxkBAAEGn9Bjh0tp3dzMwK5JO1BvSVI0yCUsAQACOw0AAtbmSFAxK-1eG55cfCsE",
                "CAACAgEAAxkBAAEGn9Rjh0z1rnIVn85ZVPXa9DZBUnkFLgACawQAAvhi8ERmUaTo2t1t_ysE",
                "CAACAgIAAxkBAAEGn9Zjh01Aw8ick5OeDUs06WTWJYcdQAACXAEAAhAabSKcIs6F61GChSsE",
                "CAACAgQAAxkBAAEGn9hjh04AAXlITxIq_Jaz10xVdTlyuH4AAkMLAALo4aBSIDcpNsGm758rBA",
                "CAACAgIAAxkBAAEGomVjiHEw3k0rKIbKRjjtmCYg06xAhQAC0RsAAhyGcUjQ7Rs7CfNrAysE",
                "CAACAgEAAxkBAAEGomdjiHSYhtzKYOODjoS-_0l60dh74QACnAIAAtscqEdAo37j6Iyu8CsE"]
osnovnaya_dir = os.getcwd()

admin_id = "437194156"
my_gf = "1047182735"
users_subs = {}  # информация о пользователях и их подписках и окончание побного периода


class User:
    """Объект пользователь с набором данных о нем"""

    def __init__(self, user_id):
        self.user_id = user_id
        user_array = open_users_data(user_id)
        if user_array is not None:
            self.fakultet = user_array[0]
            self.form = user_array[1]
            self.level = user_array[2]
            self.naprav = user_array[3]
            self.group = user_array[4]
            self.group_ftd = user_array[5]
        elif user_array is None:
            self.fakultet = self.form = self.level = self.naprav = self.group = self.group_ftd = None

    def fakult(self):
        return self.fakultet

    def get_fakult(self, fakult: str):
        self.fakultet = fakult

    def form_ob(self):
        return self.form

    def get_form_ob(self, form: str):
        self.form = form

    def level_ob(self):
        return self.level

    def get_level_ob(self, level: str):
        self.level = level

    def napr(self):
        return self.naprav

    def get_napr(self, nap: str):
        self.naprav = nap

    def gro(self):
        return self.group

    def get_gro(self, group: str):
        self.group = group

    def ftd(self):
        return self.group_ftd

    def get_ftd(self, gr_ftd):
        self.group_ftd = gr_ftd

    def subscrible_user(self):
        self.subscribe = True

    def json_create(self):
        return [self.fakultet, self.form, self.level, self.naprav, self.group, self.group_ftd]


class construct_user():
    """Создает робота для создания пользователя"""

    def open_mgou(self):
        with open("mgou.json", "r") as f:
            return json.load(f)

    def fakultet(self):
        markup = types.InlineKeyboardMarkup(row_width=1)
        fakult = list((self.open_mgou()).keys())
        for i in fakult:
            name = i.split()
            if "факультет" in name:
                name.remove("факультет")
            elif "Факультет":
                name.remove("Факультет")
            name = [name[0].title()] + name[1:]
            name = " ".join(name)
            markup.add(types.InlineKeyboardButton(name, callback_data=f"add:fakult:{abrev[i]}"))
        return markup

    def form_stud(self, us: User):
        markup = types.InlineKeyboardMarkup(row_width=1)
        fakult = us.fakult()
        mgou = self.open_mgou()
        mgou = mgou[us.fakultet]
        for i in list(mgou.keys()):
            markup.add(types.InlineKeyboardButton(i, callback_data=f"add:form:{i}"))
        markup.add(types.InlineKeyboardButton("Назад", callback_data="add:form:naz"))
        return markup

    def level(self, us: User):
        markup = types.InlineKeyboardMarkup(row_width=1)
        mgou = self.open_mgou()
        mgou = mgou[us.fakultet][us.form]
        for i in mgou:
            markup.add(types.InlineKeyboardButton(i, callback_data=f'add:level:{i}'))
        markup.add(types.InlineKeyboardButton("Назад", callback_data="add:level:naz"))
        return markup

    def naprav(self, us: User):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mg = self.open_mgou()
        napr = list(mg[us.fakultet][us.form][us.level].keys())
        for i in napr:
            markup.add(types.KeyboardButton(i))
        markup.add(types.KeyboardButton("Назад"))
        markup.add(types.KeyboardButton("Отмена"))
        return markup

    def group(self, us: User):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        timetable = open_timetable(us)
        arr = []
        for i in timetable["Учебные дисциплины"]:
            arr += list(timetable["Учебные дисциплины"][i].keys())
        arr = sorted(list(set(arr)))
        for i in arr:
            markup.add(types.KeyboardButton(i))
        markup.add(types.KeyboardButton("Назад"))
        markup.add(types.KeyboardButton("Отмена"))
        return markup

    def group_ftd(self, us: User):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        timetable = open_timetable(us)
        arr = []
        for i in timetable["ФТД"]:
            arr += list(timetable["ФТД"][i].keys())
        arr = sorted(list(set(arr)))
        for i in arr:
            markup.add(types.KeyboardButton(i))
        markup.add(types.KeyboardButton("Нет группы"))
        markup.add(types.KeyboardButton("Назад"))
        markup.add(types.KeyboardButton("Отмена"))
        return markup


const = construct_user()
mgou = const.open_mgou()


def domload_in_memory():
    with open("all_timetable.json", "r") as file:
        try:
            all_timetable = json.load(file)
        except:
            bot.send_message(admin_id, "Не получилось загрузить расписание")
    return all_timetable


all_timetable = domload_in_memory()


def open_timetable(us: User):
    """Возвращает полную базу по расписнию направления пользователя"""
    # with open(os.path.join(osnovnaya_dir,"Fakultet",us.fakultet,us.form,us.level,"group.json")) as file:
    #     timetable = json.load(file)
    # print("open")
    # return timetable[us.napr()]
    return all_timetable[us.fakult()][us.form_ob()][us.level_ob()][us.naprav]


with open("Users.json", "r") as f:
    try:
        polz = json.load(f)
        for i in polz:
            users[i] = User(i)
    except:
        users = {}
print("Все готово")
bot.send_message(admin_id, "Все готово")
# print(users)


main_menu = [[types.KeyboardButton("🗓Расписание на сегодня"), types.KeyboardButton("🗓Расписание на завтра")],
             [types.KeyboardButton("📅Календарь")],
             [types.KeyboardButton("📋Информация"), types.KeyboardButton("🔃Сменить группу")],
             [types.KeyboardButton("💰Пожертвование"), types.KeyboardButton("📝Отправить сообщение разработчику")],
             types.KeyboardButton("⚙Настройки")]
mark_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
# mark_menu.add(main_menu)
btn1 = types.KeyboardButton("🗓Расписание на сегодня")
btn2 = types.KeyboardButton("🗓Расписание на завтра")
btn3 = types.KeyboardButton("📅Календарь")
btn4 = types.KeyboardButton("🔃Сменить группу")
btn5 = types.KeyboardButton("📋Информация и контакты")
btn6 = types.KeyboardButton("💰Пожертвование")
mark_menu.add(btn1, btn2)
mark_menu.add(btn3, btn4)
mark_menu.add(btn5)
mark_menu.add(btn6)


# mark_menu.add(types.KeyboardButton("📝Отправить сообщение разработчику"))


def pairs_for_date(date, client, is_ned=False, list_dat: list = []):
    # print(type(inf_date))
    timetable = open_timetable(client)
    if not is_ned:
        if type(date) == datetime.datetime:
            inf_date = date.timetuple()
            date = date.strftime("%d.%m.%y")
        else:
            inf_date = datetime.datetime.strptime(date, "%d.%m.%y").timetuple()
        res = ""
        for i in timetable["Учебные дисциплины"]:
            if client.gro() in timetable["Учебные дисциплины"][i]:
                if date in timetable["Учебные дисциплины"][i][client.gro()]:
                    if res == "":
                        name_month = month[inf_date.tm_mon - 1].lower()
                        if name_month in ("март", "август"):
                            name_month = name_month + "а"
                        else:
                            name_month = name_month[: -1] + "я"
                        res += f"[{client.gro()}] {inf_date.tm_mday} {name_month}  {wday[inf_date.tm_wday].lower()} \n\nУчебные дисциплины\n"
                    res += f"📚 <b>{i}</b>:\n\n"
                    for pars in timetable["Учебные дисциплины"][i][client.gro()][date]:
                        res += f'🕰️ {pars}\n\n'
        res_ftd = ""
        if client.ftd() is not None:
            for i in timetable["ФТД"]:
                if client.ftd() in timetable["ФТД"][i]:
                    if date in timetable["ФТД"][i][client.ftd()]:
                        if res == "" and res_ftd == "":
                            name_month = month[inf_date.tm_mon - 1].lower()
                            if name_month in ("март", "август"):
                                name_month = name_month + "а"
                            else:
                                name_month = name_month[: -1] + "я"
                            res_ftd += f"[{client.ftd()}] {inf_date.tm_mday} {name_month}  {wday[inf_date.tm_wday].lower()} \n\nФакультативы\n"
                        elif res_ftd == "":
                            if client.ftd() != client.gro():
                                res_ftd += f"[{client.ftd()}]\nФакультативные занятия\n"
                            else:
                                res_ftd += f"Факультативные занятия\n"
                        else:
                            res_ftd += f"📚<b>{i}</b>:\n\n"
                        for pars in timetable["ФТД"][i][client.gro()][date]:
                            res_ftd += f'🕰️ {pars}\n\n'
        if res == "" and res_ftd == "":
            return "В этот день у вас нет пар"
        elif res != "" or res_ftd != "":
            return str(res + "\n" + res_ftd)
    elif is_ned:
        result = ["", ""]
        res = ""
        for day in list_dat:
            date = day.strftime("%d.%m.%y")
            inf_date = day.timetuple()
            for i in timetable["Учебные дисциплины"]:
                if client.gro() in timetable["Учебные дисциплины"][i]:
                    if date in timetable["Учебные дисциплины"][i][client.gro()]:
                        if res == "":
                            name_month = month[inf_date.tm_mon - 1].lower()
                            if name_month in ("март", "август"):
                                name_month = name_month + "а"
                            else:
                                name_month = name_month[: -1] + "я"
                            res += f"📅{inf_date.tm_mday} {name_month}  {wday[inf_date.tm_wday].lower()} \n\nУчебные дисциплины\n"
                        res += f"📚 <b>{i}</b>:\n\n"
                        for pars in timetable["Учебные дисциплины"][i][client.gro()][date]:
                            res += f'🕰️ {pars}\n\n'
            if res != "":
                res += "-" * 26 + "\n"
                result[0] += res
            res = ""
            res_ftd = ""
            if client.ftd() is not None:
                for i in timetable["ФТД"]:
                    if client.ftd() in timetable["ФТД"][i]:
                        if date in timetable["ФТД"][i][client.ftd()]:
                            if res_ftd == "":
                                name_month = month[inf_date.tm_mon - 1].lower()
                                if name_month in ("март", "август"):
                                    name_month = name_month + "а"
                                else:
                                    name_month = name_month[: -1] + "я"
                                res_ftd += f"📅{inf_date.tm_mday} {name_month}  {wday[inf_date.tm_wday].lower()} \n\n"
                            # elif res_ftd == "":
                            #     if client.ftd() != client.gro():
                            #         res_ftd += f"[{client.ftd()}]\nФакультативные занятия\n"
                            #     else:
                            #         res_ftd += f"Факультативные занятия\n"
                            else:
                                res_ftd += f"📚<b>{i}</b>:\n\n"
                            for pars in timetable["ФТД"][i][client.gro()][date]:
                                res_ftd += f'🕰️ {pars}\n\n'
            if res_ftd != "":
                result[1] += res_ftd
            res_ftd = ""
        return result


@bot.callback_query_handler(func=lambda call: "calend" in call.data.split(":") or call.data == "_")
def calendar_handler(call: types.CallbackQuery):
    if str(call.message.chat.id) not in activ_us:
        activ_us.append(str(call.message.chat.id))
    global req
    req += 1
    if call.data == "_":
        bot.answer_callback_query(call.id, "Вы не туда нажали")
    else:
        data_arr = call.data.split(":")
        operation = data_arr[1]
        client = users[str(call.message.chat.id)]
        if operation == "seg":
            date = dt.datetime.now()
            info = date.timetuple()
            calendar_menu_mark = types.InlineKeyboardMarkup(row_width=2)
            seg = types.InlineKeyboardButton("Расписание на сегодня", callback_data="calend:seg")
            zav = types.InlineKeyboardButton("Расписание на завтра", callback_data="calend:zav")
            calend = types.InlineKeyboardButton("Календарь", callback_data=f"calend:cal:{info.tm_mon}:{info.tm_year}")
            calendar_menu_mark.add(seg, zav)
            calendar_menu_mark.add(calend)
            try:
                bot.edit_message_text(pairs_for_date(date, client), call.message.chat.id,
                                      call.message.message_id, reply_markup=calendar_menu_mark)
                bot.answer_callback_query(call.id)
            except:
                if pairs_for_date(date, client) == "В этот день у вас нет пар":
                    bot.edit_message_text("В этот день тоже нет пар", call.message.chat.id,
                                          call.message.message_id, reply_markup=calendar_menu_mark)
                else:
                    bot.answer_callback_query(call.id, "Расписание осталось таким-же")
        elif operation == "zav":
            date = dt.datetime.now()
            date = date + dt.timedelta(1)
            info = date.timetuple()
            calendar_menu_mark = types.InlineKeyboardMarkup(row_width=2)
            seg = types.InlineKeyboardButton("Расписание на сегодня", callback_data="calend:seg")
            zav = types.InlineKeyboardButton("Расписание на завтра", callback_data="calend:zav")
            calend = types.InlineKeyboardButton("Календарь", callback_data=f"calend:cal:{info.tm_mon}:{info.tm_year}")
            calendar_menu_mark.add(seg, zav)
            calendar_menu_mark.add(calend)
            pairs = pairs_for_date(date, client)
            # if pairs == call.message.text:
            try:
                bot.edit_message_text(pairs_for_date(date, client), call.message.chat.id,
                                      call.message.message_id, reply_markup=calendar_menu_mark)
                bot.answer_callback_query(call.id)
            except:
                if pairs_for_date(date, client) == "В этот день у вас нет пар":
                    bot.edit_message_text("В этот день тоже нет пар", call.message.chat.id,
                                          call.message.message_id, reply_markup=calendar_menu_mark)
                else:
                    bot.answer_callback_query(call.id, "Расписание осталось таким-же")

        elif operation == "cal":
            bot.answer_callback_query(call.id)
            mon = int(data_arr[2])
            year = int(data_arr[3])
            bot.edit_message_text("Выберите дату:", call.message.chat.id, call.message.message_id,
                                  reply_markup=make_calendar_markup(mon, year, client))
        elif operation == "comand":
            comand = data_arr[2]
            mes = int(data_arr[3])
            year = int(data_arr[4])
            dat = datetime.datetime.now().timetuple()
            if dat.tm_mon <= 7:
                period = (dat.tm_year - 1, dat.tm_year)
            else:
                period = (dat.tm_year, dat.tm_year + 1)
            dat = datetime.date(int(year), int(mes), 15)
            if comand == "<":
                dat = dat - dt.timedelta(32)
                inf = dat.timetuple()
                if inf.tm_mon > 7 and inf.tm_year == period[0] or inf.tm_mon <= 7 and inf.tm_year == period[1]:
                    bot.edit_message_text(chat_id=str(call.message.chat.id), message_id=call.message.message_id,
                                          text="Выберете дату:",
                                          reply_markup=make_calendar_markup(inf.tm_mon, inf.tm_year, client))
                else:
                    bot.answer_callback_query(call.id, show_alert=False, text="Дальше нельзя")
            elif comand == ">":
                dat = dat + dt.timedelta(32)
                inf = dat.timetuple()
                if inf.tm_mon > 7 and inf.tm_year == period[0] or inf.tm_mon <= 7 and inf.tm_year == period[1]:
                    bot.edit_message_text(chat_id=str(call.message.chat.id), message_id=call.message.message_id,
                                          text="Выберете дату:",
                                          reply_markup=make_calendar_markup(inf.tm_mon, inf.tm_year,
                                                                            client))
                else:
                    bot.answer_callback_query(call.id, show_alert=False, text="Дальше нельзя")
        elif operation == "day":
            date = data_arr[2]
            mon = int(data_arr[3])
            year = int(data_arr[4])
            calendar_menu_mark = types.InlineKeyboardMarkup(row_width=2)
            seg = types.InlineKeyboardButton("Расписание на сегодня", callback_data="calend:seg")
            zav = types.InlineKeyboardButton("Расписание на завтра", callback_data="calend:zav")
            calend = types.InlineKeyboardButton("Календарь", callback_data=f"calend:cal:{mon}:{year}")
            calendar_menu_mark.add(seg, zav)
            calendar_menu_mark.add(calend)
            bot.edit_message_text(text=pairs_for_date(date, client),
                                  chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=calendar_menu_mark)
        elif operation == "ned":
            dat = data_arr[2]
            dat = dt.datetime.strptime(dat, "%d.%m.%y")
            first = dat
            days = []
            while dat.timetuple().tm_wday >= 1:
                dat = dat - dt.timedelta(1)
            if dat.timetuple().tm_wday < 6:
                if check_pairs(dat, users[str(call.message.chat.id)]):
                    days.append(dat)
            while True:
                dat = dat + dt.timedelta(1)
                if dat.timetuple().tm_wday < 6:
                    if check_pairs(dat, users[str(call.message.chat.id)]):
                        days.append(dat)
                else:
                    mark = types.InlineKeyboardMarkup(row_width=2)
                    seg = types.InlineKeyboardButton("Расписание на сегодня", callback_data="calend:seg")
                    zav = types.InlineKeyboardButton("Расписание на завтра", callback_data="calend:zav")
                    calend = types.InlineKeyboardButton("Календарь",
                                                        callback_data=f"calend:cal:{first.timetuple().tm_mon}:{first.timetuple().tm_year}")
                    mark.add(seg, zav)
                    mark.add(calend)
                    if days != []:
                        res = pairs_for_date(dt.datetime.now(), users[str(call.message.chat.id)], True, days)

                        if users[str(call.message.chat.id)].ftd() is None or (res[1] == "" and res[0] != ""):
                            bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id,
                                                  text=f"[{users[str(call.message.chat.id)].gro()}]\n{res[0]}",
                                                  reply_markup=mark)
                        elif users[str(call.message.chat.id)].ftd() is not None and res[1] != "" and res[0] != "":
                            bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id,
                                                  text=f"[{users[str(call.message.chat.id)].gro()}]\n{res[0]}\n"
                                                       f"[{users[str(call.message.chat.id)].ftd()}]\n{res[1]}",
                                                  reply_markup=mark)
                        elif users[str(call.message.chat.id)].ftd() is not None and res[1] != "" and res[0] == "":
                            bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id,
                                                  text=f"[{users[str(call.message.chat.id)].ftd()}]\n{res[1]}",
                                                  reply_markup=mark)
                        elif res[1] == "" and res[0] == "":
                            bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id,
                                                  text=f"На этой неделе нет у вас пар",
                                                  reply_markup=mark)
                        break
                    else:
                        bot.send_message(call.message.chat.id, "На данной неделе нет пар", reply_markup=mark)
                        break


def check_pairs(date, client):
    "Проверяет есть ли пары"
    inf_date = date.timetuple()
    date = date.strftime("%d.%m.%y")
    timetable = open_timetable(client)
    for i in timetable["Учебные дисциплины"]:
        if client.gro() in timetable["Учебные дисциплины"][i]:
            if date in timetable["Учебные дисциплины"][i][client.gro()]:
                return True
    if client.ftd() is not None:
        for i in timetable["ФТД"]:
            if client.ftd() in timetable["ФТД"][i]:
                if date in timetable["ФТД"][i][client.ftd()]:
                    return True
    return False


def make_calendar_markup(mes, year, client):
    "Создает инлайновый календарь"

    markup = telebot.types.InlineKeyboardMarkup(row_width=7)
    title = telebot.types.InlineKeyboardButton(year, callback_data="_")
    markup.add(title)
    timetable = open_timetable(client)
    wd1 = telebot.types.InlineKeyboardButton("Пн", callback_data="_")
    wd2 = telebot.types.InlineKeyboardButton("Вт", callback_data="_")
    wd3 = telebot.types.InlineKeyboardButton("Ср", callback_data="_")
    wd4 = telebot.types.InlineKeyboardButton("Чт", callback_data="_")
    wd5 = telebot.types.InlineKeyboardButton("Пт", callback_data="_")
    wd6 = telebot.types.InlineKeyboardButton("Сб", callback_data="_")
    wdned = telebot.types.InlineKeyboardButton("Нед", callback_data="_")
    markup.add(wd1, wd2, wd3, wd4, wd5, wd6, wdned)
    yestday = dt.datetime.now()
    yestday = yestday.strftime('%d.%m.%y')
    cnt = 0
    mass = ["_"] * 6
    "•📖🟢"
    for i in range(1, 32):
        try:
            dat = datetime.date(year, mes, i)
        except:
            if any(i != "_" for i in mass):
                days_arr = []
                first = None
                for first_day in mass:
                    if str(first_day).isdigit():
                        first = dt.date(year, mes, first_day)
                        first = first.strftime("%d.%m.%y")
                        break
                for k in mass:
                    if k != "_":
                        day = datetime.date(year, mes, k)  # Генерируем день
                        if check_pairs(day, client):
                            if day.strftime('%d.%m.%y') == yestday:
                                days_arr.append(types.InlineKeyboardButton(f"{k}🔵",
                                                                           callback_data=f"calend:day:{day.strftime('%d.%m.%y')}"
                                                                                         f":{mes}:{year}"))
                            else:
                                days_arr.append(types.InlineKeyboardButton(f"{k}📖",
                                                                           callback_data=f"calend:day:{day.strftime('%d.%m.%y')}"
                                                                                         f":{mes}:{year}"))

                        else:
                            if day.strftime('%d.%m.%y') == yestday:
                                days_arr.append(types.InlineKeyboardButton(f"{k}•",
                                                                           callback_data=f"calend:day:{day.strftime('%d.%m.%y')}:{mes}:{year}"))
                            else:
                                days_arr.append(types.InlineKeyboardButton(f"{k}",
                                                                           callback_data=f"calend:day:{day.strftime('%d.%m.%y')}:{mes}:{year}"))

                    else:
                        days_arr.append(types.InlineKeyboardButton("—",
                                                                   callback_data="_"))
                cnt += 1
                markup.add(days_arr[0], days_arr[1], days_arr[2],
                           days_arr[3], days_arr[4], days_arr[5],
                           types.InlineKeyboardButton(f"|{cnt}|", callback_data=f"calend:ned:{first}"))
            break
        inf = dat.timetuple()
        if inf.tm_wday < 6:
            mass[inf.tm_wday] = i
        if inf.tm_wday == 5:
            days_arr = []
            first = None
            for first_day in mass:
                if str(first_day).isdigit():
                    first = dt.date(year, mes, first_day)
                    first = first.strftime("%d.%m.%y")
                    break
            for i in mass:
                if i != "_":
                    day = datetime.date(year, mes, i)  # Генерируем день
                    if check_pairs(day, client):
                        if day.strftime('%d.%m.%y') == yestday:
                            days_arr.append(types.InlineKeyboardButton(f"{i}🔵",
                                                                       callback_data=f"calend:day:{day.strftime('%d.%m.%y')}:{mes}:{year}"))
                        else:
                            days_arr.append(types.InlineKeyboardButton(f"{i}📖",
                                                                       callback_data=f"calend:day:{day.strftime('%d.%m.%y')}:{mes}:{year}"))

                    else:
                        if day.strftime('%d.%m.%y') == yestday:
                            days_arr.append(types.InlineKeyboardButton(f"{i}•",
                                                                       callback_data=f"calend:day:{day.strftime('%d.%m.%y')}:{mes}:{year}"))
                        else:
                            days_arr.append(types.InlineKeyboardButton(f"{i}",
                                                                       callback_data=f"calend:day:{day.strftime('%d.%m.%y')}:{mes}:{year}"))

                else:
                    days_arr.append(types.InlineKeyboardButton("—",
                                                               callback_data="_"))
            cnt += 1
            markup.add(days_arr[0], days_arr[1], days_arr[2], days_arr[3], days_arr[4], days_arr[5],
                       types.InlineKeyboardButton(f"|{cnt}|", callback_data=f"calend:ned:{first}"))
            mass = ["_"] * 6
    else:
        if any(i != "_" for i in mass):
            days_arr = []
            first = None
            for first_day in mass:
                if str(first_day).isdigit():
                    first = dt.date(year, mes, first_day)
                    first = first.strftime("%d.%m.%y")
                    break
            for k in mass:
                if k != "_":
                    day = datetime.date(year, mes, k)  # Генерируем день
                    if check_pairs(day, client):
                        if day.strftime('%d.%m.%y') == yestday:
                            days_arr.append(types.InlineKeyboardButton(f"{k}🔵",
                                                                       callback_data=f"calend:day:"
                                                                                     f"{day.strftime('%d.%m.%y')}"
                                                                                     f":{mes}:{year}"))
                        else:
                            days_arr.append(types.InlineKeyboardButton(f"{k}📖",
                                                                       callback_data=f"calend:day:"
                                                                                     f"{day.strftime('%d.%m.%y')}"
                                                                                     f":{mes}:{year}"))

                    else:
                        if day.strftime('%d.%m.%y') == yestday:
                            days_arr.append(types.InlineKeyboardButton(f"{k}•",
                                                                       callback_data=f"calend:day"
                                                                                     f":{day.strftime('%d.%m.%y')}"
                                                                                     f":{mes}:{year}"))
                        else:
                            days_arr.append(types.InlineKeyboardButton(f"{k}",
                                                                       callback_data=f"calend:day"
                                                                                     f":{day.strftime('%d.%m.%y')}"
                                                                                     f":{mes}:{year}"))
                else:
                    days_arr.append(types.InlineKeyboardButton("—",
                                                               callback_data="_"))
            cnt += 1
            markup.add(days_arr[0], days_arr[1], days_arr[2], days_arr[3], days_arr[4], days_arr[5],
                       types.InlineKeyboardButton(f"|{cnt}|", callback_data=f"calend:ned:{first}"))
    nalev = telebot.types.InlineKeyboardButton("<=",
                                               callback_data=f"calend:comand:<:{mes}:{year}")
    mesyac = telebot.types.InlineKeyboardButton(month[mes - 1],
                                                callback_data="_")
    napravo = telebot.types.InlineKeyboardButton("=>",
                                                 callback_data=f"calend:comand:>:{mes}:{year}")
    markup.add(nalev, mesyac, napravo)
    zav = telebot.types.InlineKeyboardButton("Расписание на завтра", callback_data="calend:zav")
    seg = telebot.types.InlineKeyboardButton("Расписание на сегодня", callback_data="calend:seg")
    markup.add(seg, zav)
    return markup


@bot.callback_query_handler(func=lambda call: "add" in call.data.split(":"))
def add_user(call):
    mes_id = str(call.message.chat.id)
    arr_inf = call.data.split(":")
    type_hand = arr_inf[1]
    info = arr_inf[2]
    if info == "naz":
        if type_hand == "form":
            bot.edit_message_text("Выберите факультет: ", call.message.chat.id, call.message.message_id,
                                  reply_markup=const.fakultet())
        elif type_hand == "level":
            bot.edit_message_text("Выберите форму обучения: ", call.message.chat.id, call.message.message_id,
                                  reply_markup=const.form_stud(users[str(call.message.chat.id)]))
    elif type_hand == "fakult":
        users[mes_id].get_fakult(abrev_rash[info])
        bot.edit_message_text("Выберите форму обучения: ", call.message.chat.id, call.message.message_id,
                              reply_markup=const.form_stud(users[mes_id]))
    elif type_hand == "form":
        users[mes_id].get_form_ob(info)
        bot.edit_message_text("Выберите уровень: ", call.message.chat.id, call.message.message_id,
                              reply_markup=const.level(users[mes_id]))
    elif type_hand == "level":
        users[mes_id].get_level_ob(info)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        send = bot.send_message(mes_id, "Выберите с помощью кнопок ниже ваше направление: ",
                                reply_markup=const.naprav(users[mes_id]))
        bot.register_next_step_handler(send, choice_napr)
    elif type_hand == "reg":
        if str(call.message.chat.id) not in users:
            us = User(str(call.message.chat.id))
            users[str(call.message.chat.id)] = us
        users[str(call.message.chat.id)] = User(str(call.message.chat.id))
        bot.edit_message_text("Выберите факультет:", call.message.chat.id, call.message.message_id,
                              reply_markup=const.fakultet())


def choice_napr(message):
    client = users[str(message.chat.id)]
    # print("Это направление")
    with open("mgou.json", "r") as file:
        napr = sorted(list((json.load(file)[client.fakult()][client.form_ob()][client.level_ob()]).keys()))
    if message.text in napr:
        users[str(message.chat.id)].get_napr(message.text)
        send = bot.send_message(message.chat.id, "Выберите вашу группу: ",
                                reply_markup=const.group(users[str(message.chat.id)]))
        bot.register_next_step_handler(send, choice_group)
    elif message.text == "Отмена":
        bot.send_message(message.chat.id,
                         "Действие отменено, если хотите перейти к выбору направления, то введите команду "
                         "\"\\start\", \"\\change_group\", или смените группу с помощью кнопки внизу"
                         , reply_markup=mark_menu)
    elif message.text == "Назад":
        bot.send_message(message.chat.id, "Выберите уровень: ", reply_markup=const.level(client))
        types.ReplyKeyboardRemove()
    elif message.text not in napr:
        message.text = str(message.text).replace("…", "")
        # print(message.text)
        maibi = []
        for k in napr:
            flag = True
            for i in str(message.text).split():
                if i not in k:
                    flag = False
                    # print(k)
                    break
            if flag:
                maibi.append(k)
        if len(maibi) == 1:
            users[str(message.chat.id)].get_napr(maibi[0])
            send = bot.send_message(message.chat.id, "Выберите вашу группу: ",
                                    reply_markup=const.group(users[str(message.chat.id)]))
            bot.register_next_step_handler(send, choice_group)
        else:
            send = bot.send_message(message.chat.id,
                                    "Такого нет направления на вашем факультете, выберете подходящий с помощью кнопок "
                                    "внизу чата")
            bot.register_next_step_handler(send, choice_napr)


def choice_group(message):
    client = users[str(message.chat.id)]
    all_gr = []
    with open(os.path.join("Fakultet", client.fakult(), client.form_ob(), client.level_ob(), "group.json")) as file:
        group = json.load(file)[client.napr()]
        for i in group["Учебные дисциплины"]:
            all_gr += list(group["Учебные дисциплины"][i].keys())
    all_gr = list(set(all_gr))
    for i in range(len(all_gr)):
        all_gr[i] = all_gr[i].replace(" ", "")
    # print(all_gr)
    if message.text in all_gr:
        for gru in all_gr:
            if message.text in gru:
                users[str(message.chat.id)].get_gro(gru)
                if any(group["ФТД"][i] != {} for i in group["ФТД"]):
                    send = bot.send_message(message.chat.id,
                                            "Выберите ваш факультатив согласно таблицы с расписанием, если же у вас нет факультатива"
                                            "нажмите на кнопку\"нет группы\": ",
                                            reply_markup=const.group_ftd(users[str(message.chat.id)]))
                    bot.register_next_step_handler(send, choice_group_ftd)
                else:
                    users[str(message.chat.id)].get_ftd(None)
                    client = users[str(message.chat.id)]
                    bot.send_message(message.chat.id, f"Ваши данные теперь таковы\n"
                                                      f"Факультет: {client.fakult()}\n"
                                                      f"Форма обучения: {client.form_ob()}\n"
                                                      f"Уровень: {client.level_ob()}\n"
                                                      f"Направление: {client.napr()}\n"
                                                      f"Группа: {client.gro()}\n", reply_markup=mark_menu)
                with open("Users.json", "r") as file:
                    try:
                        all_user = json.load(file)
                    except:
                        all_user = {}
                with open("Users.json", "w") as file:
                    if str(message.chat.id) in all_user:
                        del all_user[str(message.chat.id)]
                    all_user[str(message.chat.id)] = users[str(message.chat.id)].json_create()
                    json.dump(all_user, file, ensure_ascii=True, indent=2)

    elif message.text == "Отмена":
        bot.send_message(message.chat.id,
                         "Действие отменено, если хотите перейти к выбору направления, то введите команду "
                         "\"\\start\", \"\\change_group\", или смените группу с помощью кнопки внизу"
                         , reply_markup=mark_menu)


    elif message.text == "Назад":
        send = bot.send_message(message.chat.id, "Выберите пожалуйста направление:", reply_markup=const.naprav(client))
        bot.register_next_step_handler(send, choice_napr)

    elif message.text not in all_gr:
        send = bot.send_message(message.chat.id,
                                "Такой группы нет на вашем факультете, выберете подходящий с помощью кнопок "
                                "внизу чата")
        bot.register_next_step_handler(send, choice_group)


def choice_group_ftd(message):
    client = users[str(message.chat.id)]
    all_gr = []
    with open(os.path.join("Fakultet", client.fakult(), client.form_ob(), client.level_ob(), "group.json")) as file:
        group = json.load(file)[client.napr()]
        for i in group["ФТД"]:
            all_gr += list(group["ФТД"][i].keys())
    all_gr = list(set(all_gr))
    for i in range(len(all_gr)):
        all_gr[i] = all_gr[i].replace(" ", "")
    if message.text in all_gr:
        users[str(message.chat.id)].get_ftd(message.text)
        client = users[str(message.chat.id)]
        bot.send_message(message.chat.id, f"Ваши данные теперь таковы\n"
                                          f"<b>Факультет</b>: {client.fakult()}\n"
                                          f"<b>Форма обучения</b>: {client.form_ob()}\n"
                                          f"<b>Уровень</b>: {client.level_ob()}\n"
                                          f"<b>Направление</b>: {client.napr()}\n"
                                          f"<b>Группа</b>: {client.gro()}\n"
                                          f"<b>Факультатив</b>: {client.ftd()}", reply_markup=mark_menu)
        with open("Users.json", "r") as file:
            try:
                all_user = json.load(file)
            except:
                all_user = {}
        with open("Users.json", "w") as file:
            if str(message.chat.id) in all_user:
                del all_user[str(message.chat.id)]
            all_user[str(message.chat.id)] = users[str(message.chat.id)].json_create()
            json.dump(all_user, file, ensure_ascii=True, indent=2)

    elif message.text == "Нет группы":
        users[str(message.chat.id)].get_ftd(None)
        client = users[str(message.chat.id)]
        bot.send_message(message.chat.id, f"Ваши данные теперь таковы\n"
                                          f"<b>Факультет</b>: {client.fakult()}\n"
                                          f"<b>Форма обучения</b>: {client.form_ob()}\n"
                                          f"<b>Уровень</b>: {client.level_ob()}\n"
                                          f"<b>Направление</b>: {client.napr()}\n"
                                          f"<b>Группа</b>: {client.gro()}\n"
                                          f"<b>Факультатив: Нет</b>", reply_markup=mark_menu)
        with open("Users.json", "r") as file:
            try:
                all_user = json.load(file)
            except:
                all_user = {}
        with open("Users.json", "w") as file:
            if str(message.chat.id) in all_user:
                del all_user[str(message.chat.id)]
            all_user[str(message.chat.id)] = users[str(message.chat.id)].json_create()
            json.dump(all_user, file, ensure_ascii=True, indent=2)
    elif message.text == "Отмена":
        bot.send_message(message.chat.id,
                         "Действие отменено, если хотите перейти к выбору направления, то введите команду "
                         "\"\\start\", \"\\change_group\", или смените группу с помощью кнопки внизу"
                         , reply_markup=mark_menu)
    elif message.text == "Назад":
        send = bot.send_message(message.chat.id, "Выберите группу:", reply_markup=const.group(client))
        bot.register_next_step_handler(send, choice_group)
    elif message.text not in all_gr:
        send = bot.send_message(message.chat.id,
                                "Такой группы нет на вашем факультете, выберете подходящий с помощью кнопок "
                                "внизу чата")
        bot.register_next_step_handler(send, choice_group_ftd)


# "Для последующей смены группы введите \"\\start\", \"\\change_group\""
#                                           f"или нажмите на соответсвующую кнопку\n\n"
# "<b>VK</b>?: <a href='https://vk.com/ygoryochek'>ygoryochek</a>\n"

def send_for_admin(message, user_mes: str = "", is_send_flag=False, is_editing_mes=False):
    message.text = clear_emoji(message.text)
    if "отмена" == str(message.text).lower():
        bot.send_message(message.chat.id, "Отправка сообщения разработчику отклонено", reply_markup=mark_menu)
    elif "отправить" == str(message.text).lower():
        mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mark.add(types.KeyboardButton("✔Да"))
        mark.add(types.KeyboardButton("❌Нет"))
        mark.add(types.KeyboardButton("✏Редактировать"))
        send = bot.send_message(message.chat.id, "Вы точно хотите отправить сообщение разработчику?", reply_markup=mark)
        bot.register_next_step_handler(send, send_for_admin, user_mes, True)
    elif 'да' == str(message.text).lower() and is_send_flag:
        bot.send_message(message.chat.id, "Сообщение отправленно разработчику", reply_markup=mark_menu)
        bot.send_message(admin_id, f"#сообщение \n@ygoryochek , пришло новое сообщение от пользователя\n"
                                   f"ID пользователя: {message.from_user.id}\n"
                                   f"Имя: {message.from_user.first_name}\n"
                                   f"Фамилия: {message.from_user.last_name}\n"
                                   f"Username: @{message.from_user.username}\n"
                                   f"Текст сообщения: {user_mes}")
    elif 'нет' == str(message.text).lower() and is_send_flag:
        bot.send_message(message.chat.id, "Отправка сообщения отменена", reply_markup=mark_menu)
    elif 'редактировать' == str(message.text).lower():
        if user_mes == "":
            send = bot.send_message(message.chat.id, "Ваше сообщение пустое вам нечего редактировать")
            bot.register_next_step_handler(send, send_for_admin, user_mes, False, True)
        else:
            bot.send_message(message.chat.id,
                             "Для редактирования сообщения вы можете скопировать свой текст и отправить его заново\n"
                             "На данный момент ваш текст выглядит так:")
            send = bot.send_message(message.chat.id, f"{user_mes}")
            bot.register_next_step_handler(send, send_for_admin, user_mes, False, True)
    elif is_editing_mes:
        user_mes = message.text
        mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mark.add(types.KeyboardButton("📦Отправить"))
        mark.add(types.KeyboardButton("❌Отмена"))
        mark.add(types.KeyboardButton("✏Редактировать"))
        send = bot.send_message(message.chat.id, "Сообщение отредактировано, если вы готовы его отправить, "
                                                 "то нажмите на кнопку \"Отправить\"", reply_markup=mark)
        bot.register_next_step_handler(send, send_for_admin, user_mes)
    elif str(message.text).lower() != "отправить":
        user_mes += str(message.text)
        mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mark.add(types.KeyboardButton("📦Отправить"))
        mark.add(types.KeyboardButton("❌Отмена"))
        mark.add(types.KeyboardButton("✏Редактировать"))
        send = bot.send_message(message.chat.id, "Сообщение записано, если вы готовы его отправить, "
                                                 "то нажмите на кнопку \"Отправить\"", reply_markup=mark)
        bot.register_next_step_handler(send, send_for_admin, user_mes)


def mes_for_all(message, sending_message, sen_all=False, is_editing_mes=False):
    if str(message.text).lower() == "отмена":
        bot.send_message(message.chat.id, "Отправка сообщени отклонена", reply_markup=mark_menu)
    if str(message.text).lower() == "отправить":
        mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mark.add(types.KeyboardButton("Да"))
        mark.add(types.KeyboardButton("Нет"))
        send = bot.send_message(admin_id, "Вы точно желаете отправить соообщение всем пользователям?",
                                reply_markup=mark)
        bot.register_next_step_handler(send, mes_for_all, sending_message, True)
    elif "да" in str(message.text).lower() and sen_all:
        bot.send_message(admin_id, "Начинаю отправку сообщений", reply_markup=mark_menu)
        for i in users:
            if i != admin_id:
                bot.send_message(i, sending_message)
                time.sleep(1)
    elif str(message.text).lower() == "нет" and sen_all or str(message.text).lower() == "отмена":
        bot.send_message(admin_id, "Хорошо, тогда не буду отправлять всем сообщение", reply_markup=mark_menu)
    elif str(message.text).lower() == 'редактировать':
        bot.send_message(message.chat.id,
                         "Для редактирования сообщения вы можете скопировать свой текст и отправить его заново\n"
                         "На данный момент ваш текст выглядит так:")
        send = bot.send_message(message.chat.id, f"{sending_message}")
        bot.register_next_step_handler(send, mes_for_all, sending_message, False, True)
    elif is_editing_mes:
        sending_message = message.text
        mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mark.add(types.KeyboardButton("Отправить"))
        mark.add(types.KeyboardButton("Отмена"))
        mark.add(types.KeyboardButton("Редактировать"))
        send = bot.send_message(message.chat.id, "Сообщение отредактировано, если вы готовы его отправить, "
                                                 "то нажмите на кнопку \"Отправить\"", reply_markup=mark)
        bot.register_next_step_handler(send, mes_for_all, sending_message)
    elif str(message.text).lower() != "отправить":
        sending_message += str(message.text)
        mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mark.add(types.KeyboardButton("Отправить"))
        mark.add(types.KeyboardButton("Отмена"))
        mark.add(types.KeyboardButton("Редактировать"))
        send = bot.send_message(message.chat.id, "Сообщение записано, если вы готовы его отправить, "
                                                 "то нажмите на кнопку \"Отправить\"", reply_markup=mark)
        bot.register_next_step_handler(send, mes_for_all, sending_message)


def clear_emoji(message: str):
    arr_emoji = ["✔", "🗓", "📅", "🔃", "📋", "💰", "📝", "📦", "❌", "✏"]
    if any(i in arr_emoji for i in arr_emoji):
        for k in arr_emoji:
            message = message.replace(k, "")
    return message


@bot.message_handler(commands=["update", "send_all", "mark", "info_users"],
                     func=lambda message: str(message.chat.id) == admin_id)
def admins_commands(message):
    if message.text == "/mark":
        bot.send_message(message.chat.id, "Обновлено маркап", reply_markup=mark_menu)
    elif message.text == "/update":
        bot.send_message(message.chat.id, "Начал обнову")
        bot.send_message(message.chat.id, "Обновляю базу расписаний")
        update()
        bot.send_message(message.chat.id, "Загружаю расписание групп")
        upload_rasp()
        bot.send_message(message.chat.id, "Загрузка произошла успешно")
        os.chdir(osnovnaya_dir)
        global all_timetable
        all_timetable = domload_in_memory()
    elif message.text == "/send_all":
        mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mark.add(types.KeyboardButton("Отправить"))
        mark.add(types.KeyboardButton("Отмена"))
        send = bot.send_message(admin_id, "Введите текст своего сообщения для всех пользователей", reply_markup=mark)
        bot.register_next_step_handler(send, mes_for_all, "")
    elif message.text == "/info_users":
        bot.send_message(admin_id, f"Людей использовало: {len(activ_us)}\n"
                                   f"Всего запросов: {req}\n"
                                   f"Людей зарегистрировано: {len(users.keys())}")


# f"Здравствуйте {message.chat.first_name} {message.chat.last_name if message.chat.last_name != None else ''}."
# f"Я бот, созданный для удобства использования расписанием ВУЗА \"МГОПУ\""
# f"В данный момент бот запущен в тестовом режиме и каждому доступен весь его функционал."
# f"Поэтому в случае, если вы увидите какую либо ошибку в работе бота, отправьте разработчику сообщение об этом с помощью кнопки: \"Отправить сообщение разработчику\""
# f"‼После завершения тестового режима, ботом можно будет пользоваться по небольшой подписке, но будет доступен 14 дневный пробный период‼"
# f"Важно!!! перед использованием бота, проверьте расписание на соответсвие с вашей таблицей Excel"
@bot.message_handler(
    commands=['start', "today", "tomorrow", "calendar", "change_group", "information", "update", "donat", "reload"])
def main_commands(message):
    if str(message.chat.id) not in activ_us:
        activ_us.append(str(message.chat.id))
    global req
    req += 1
    date = dt.datetime.now()
    info = date.timetuple()
    if message.text == "/start":
        mark = types.InlineKeyboardMarkup(row_width=1)
        short_mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
        short_mark.add(types.KeyboardButton("📋Информация и контакты"), types.KeyboardButton("💰Пожертвование"))
        short_mark.add(types.KeyboardButton("📝Отправить сообщение разработчику"))
        mark.add(types.InlineKeyboardButton("✔Зарегистрироваться", callback_data="add:reg:reg"))
        bot.send_message(message.chat.id,
                         f"Здравствуйте {message.chat.first_name} {message.chat.last_name if message.chat.last_name != None else ''}.\n"
                         f"Я бот, созданный для удобного использования расписания ВУЗА \"ГУП\"\n"
                         f"В данный момент бот запущен в тестовом режиме и каждому доступен весь его функционал.\n"
                         f"Поэтому, в случае, если вы увидите какую либо ошибку в работе бота, отправьте разработчику сообщение об этом с помощью кнопки: \"Отправить сообщение разработчику\""
                         f"‼После завершения тестового режима, ботом можно будет пользоваться по небольшой подписке, но будет доступен 14 дневный пробный период‼\n"
                         f"Важно!!! перед использованием бота, проверьте расписание на соответсвие с вашей таблицей Excel",
                         reply_markup=short_mark)
        bot.send_message(message.chat.id, f"Для начала процедуры регистрации "
                                          f"нажмите на кнопку под сообщением", reply_markup=mark)
    elif message.text == "/change_group":
        bot.send_message(message.chat.id, "Выберите пожалуйста факультет: ", reply_markup=const.fakultet())
    elif message.text == "/reload":
        bot.send_message(message.chat.id, "Клавиатура обновлена", reply_markup=mark_menu)
    elif message.text == "/information":
        info_table = types.InlineKeyboardMarkup(row_width=2)
        git = "https://github.com/Heldash"
        telegram_lichka = "https://t.me/ygoryochek"
        vk = "https://vk.com/ygoryochek"
        tg_btn = types.InlineKeyboardButton("Телеграм", url=telegram_lichka)
        git_btn = types.InlineKeyboardButton("GitHub", url=git)
        vk_btn = types.InlineKeyboardButton("VK", url=vk)
        # info_table.add(tg_btn, git_btn)
        # info_table.add(vk_btn)
        info_table.add(git_btn)
        bot.send_message(message.chat.id, "Мой создатель Игорь Смирнов такой же студент как и вы 👨‍🎓\n"
                                          "Ссылки на соц сети и обратную связь с разработчиком\n"
                                          "-------------------------------------------------\n"
                                          "<b>Почта</b>📧: dartin.rok@yandex.ru \n"
                                          "<b>GitHub</b>💻:<a href='https://github.com/Heldash'>Heldash</a>\n"
                                          "-------------------------------------------------\n"
                                          "💰Также буду рад если поддержите меня рублем💰\n"
                                          "<strong>Сбер</strong>💳: <code>4276400102891869</code>", parse_mode="HTML",
                         disable_web_page_preview=True, reply_markup=info_table)
    elif message.text == "/donat":
        bot.send_message(message.chat.id, "Буду рад, если вы поддержите мой проект\n"
                                          "<b>Сбер</b>💳: <code>4276400102891869</code>", reply_markup=mark_menu)
    elif message.text in ("/today", "/tomorrow", "/calendar"):
        if str(message.chat.id) in users:
            if message.text == "/today":
                client = users[str(message.chat.id)]
                calendar_menu_mark = types.InlineKeyboardMarkup(row_width=2)
                seg = types.InlineKeyboardButton("Расписание на сегодня", callback_data="calend:seg")
                zav = types.InlineKeyboardButton("Расписание на завтра", callback_data="calend:zav")
                calend = types.InlineKeyboardButton("Календарь",
                                                    callback_data=f"calend:cal:{info.tm_mon}:{info.tm_year}")
                calendar_menu_mark.add(seg, zav)
                calendar_menu_mark.add(calend)
                date = dt.datetime.now()
                bot.send_message(message.chat.id, pairs_for_date(date, client), reply_markup=calendar_menu_mark)
            elif message.text == "/tomorrow":
                client = users[str(message.chat.id)]
                calendar_menu_mark = types.InlineKeyboardMarkup(row_width=2)
                seg = types.InlineKeyboardButton("Расписание на сегодня", callback_data="calend:seg")
                zav = types.InlineKeyboardButton("Расписание на завтра", callback_data="calend:zav")
                calend = types.InlineKeyboardButton("Календарь",
                                                    callback_data=f"calend:cal:{info.tm_mon}:{info.tm_year}")
                calendar_menu_mark.add(seg, zav)
                calendar_menu_mark.add(calend)
                date = dt.datetime.now()
                date = date + dt.timedelta(1)
                bot.send_message(message.chat.id, pairs_for_date(date, client), reply_markup=calendar_menu_mark)
            elif message.text == "/calendar":
                client = users[str(message.chat.id)]
                bot.send_message(message.chat.id, "Выберите дату", reply_markup=make_calendar_markup(info.tm_mon,
                                                                                                     info.tm_year,
                                                                                                     client))
        elif str(message.chat.id) not in users:
            mark = types.InlineKeyboardMarkup(row_width=1)
            reg = types.InlineKeyboardButton("Регистрация", callback_data="add:reg:reg")
            mark.add(reg)
            bot.send_message(message.chat.id, "Вы не зарегестрированы в системе, нажмите на кнопку зарегестрироваться"
                                              "или пожалуйста введите команду \"\\start\"", reply_markup=mark)
    else:
        bot.send_message(message.chat.id, "Я не знаю что это за команда ?")


# ---------------------------------------------
# ---------------------------------------------
# --------------------------------------------- Обработчики разделитель
# ---------------------------------------------


@bot.message_handler(content_types=["text"])
def text_check(message):
    message.text = clear_emoji(message.text)
    if str(message.chat.id) not in activ_us:
        activ_us.append(str(message.chat.id))
    global req
    req += 1
    date = dt.datetime.now()
    info = date.timetuple()
    # print(str(message.text))
    calendar_menu_mark = types.InlineKeyboardMarkup(row_width=2)
    seg = types.InlineKeyboardButton("Расписание на сегодня", callback_data="calend:seg")
    zav = types.InlineKeyboardButton("Расписание на завтра", callback_data="calend:zav")
    calend = types.InlineKeyboardButton("Календарь", callback_data=f"calend:cal:{info.tm_mon}:{info.tm_year}")
    calendar_menu_mark.add(seg, zav)
    calendar_menu_mark.add(calend)
    if "сменить группу" == str(message.text).lower() or "зарегестрироваться" == str(message.text).lower():
        bot.send_message(message.chat.id, "Выберите факультет: ", reply_markup=const.fakultet())
    elif "информация и контакты" == str(message.text).lower():
        info_table = types.InlineKeyboardMarkup(row_width=2)
        git = "https://github.com/Heldash"
        telegram_lichka = "https://t.me/ygoryochek"
        vk = "https://vk.com/ygoryochek"
        tg_btn = types.InlineKeyboardButton("Телеграм", url=telegram_lichka)
        git_btn = types.InlineKeyboardButton("GitHub", url=git)
        vk_btn = types.InlineKeyboardButton("VK", url=vk)
        # info_table.add(tg_btn, git_btn)
        info_table.add(git_btn)
        # info_table.add(vk_btn)
        bot.send_message(message.chat.id, "Мой создатель Игорь Смирнов такой же студент как и вы 👨‍🎓\n"
                                          "Ссылки на соц сети и обратную связь с разработчиком\n"
                                          "-------------------------------------------------\n"
                                          "<b>Почта</b>📧: dartin.rok@yandex.ru \n"
                                          "<b>GitHub</b>💻:<a href='https://github.com/Heldash'>Heldash</a>\n"
                                          "-------------------------------------------------\n"
                                          "💰Также буду рад если поддержите меня денюжкой💰\n"
                                          "<strong>Сбер</strong>💳: <code>4276400102891869</code>", parse_mode="HTML",
                         disable_web_page_preview=True, reply_markup=info_table)
    elif "пожертвование" == str(message.text).lower():
        bot.send_message(message.chat.id, "Буду рад, если вы поддержите мой проект\n"
                                          "<b>Сбер</b>: <code>4276400102891869</code>")
    elif "отправить сообщение разработчику" == str(message.text).lower():
        mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
        send = bot.send_message(message.chat.id, "Напишите сюда отзыв или сообщение разработчику, "
                                                 "если вы передумали отправлять "
                                                 "сообщение, нажмите на кнопку отмена.\n"
                                                 "Когда будете готовы отправить сообщение, нажмите на кнопку \"отправить\"")
        bot.register_next_step_handler(send, send_for_admin)
    elif str(message.text).lower() in ("расписание на сегодня", "расписание на завтра", "календарь") or re.fullmatch(
            r"\d\d\D\d\d\D\d\d", message.text):
        if str(message.chat.id) in users:
            if "расписание на сегодня" == str(message.text).lower():
                client = users[str(message.chat.id)]
                date = dt.datetime.now()
                bot.send_message(message.chat.id, pairs_for_date(date, client), reply_markup=calendar_menu_mark)
            elif "расписание на завтра" == str(message.text).lower():
                client = users[str(message.chat.id)]
                date = dt.datetime.now()
                date = date + dt.timedelta(1)
                bot.send_message(message.chat.id, pairs_for_date(date, client), reply_markup=calendar_menu_mark)
            elif "календарь" == str(message.text).lower():
                client = users[str(message.chat.id)]
                bot.send_message(message.chat.id, "Выберите дату", reply_markup=make_calendar_markup(info.tm_mon,
                                                                                                     info.tm_year,
                                                                                                     client))
            elif re.fullmatch(r"\d\d\D\d\d\D\d\d", message.text):
                try:
                    dat = dt.datetime.strptime(message.text, "%d.%m.%y")
                    bot.send_message(message.chat, pairs_for_date(dat, users[str(message.chat.id)]))
                except:
                    bot.send_message(message.chat.id, "Такой даты существует")
        elif str(message.chat.id) not in users:
            mark = types.InlineKeyboardMarkup(row_width=1)
            reg = types.InlineKeyboardButton("✔Регистрация", callback_data="add:reg:reg")
            mark.add(reg)
            bot.send_message(message.chat.id, "Вы не зарегестрированы в системе, нажмите на кнопку зарегестрироваться"
                                              "или пожалуйста введите команду \"\\start\"", reply_markup=mark)
    else:
        bot.send_message(message.chat.id, "Я не знаю что это за команда")


def updating():
    bot.send_message(admin_id, "Начал обнову")
    try:
        update()
    except:
        bot.send_message(admin_id, "Ошибка обновления расписания")
    try:
        upload_rasp()
    except:
        bot.send_message(admin_id, "Ошибка загрузки расписания групп")
    bot.send_message(admin_id, "Загрузка произошла успешно")
    os.chdir(osnovnaya_dir)
    global all_timetable
    all_timetable = domload_in_memory()
    # for fak in mgou:
    #     for form in mgou[fak]:
    #         for level in mgou[fak][form]:
    #             with open(os.path.join(osnovnaya_dir, "Fakultet", fak, form, level, "group.json")) as file:
    #                 timetable = json.load(file)
    #                 for napr in mgou[fak][form][level]:
    #                     all_timetable[fak][form][level][napr] = timetable[napr]


def updating_mgou():
    try:
        os.chdir(osnovnaya_dir)
        bot.send_message(admin_id, "Выполняю парсинг МГОУ")
        global mgou
        mgou = parsing_mgou.up_mgou(mgou, bot)
        bot.send_message(admin_id, "Парсинг выполнен успешно")
    except:
        bot.send_message(admin_id, "Не удалось обновить данные по ссылкам милорд")
    parsing_mgou.proff_parsing()


def statist():
    global req
    global activ_us
    for i in users:
        pass
    bot.send_message(admin_id, f"#Отчет\n"
                               f"На {datetime.datetime.now().strftime('%d.%m.%y')}\n"
                               f"Пользователей воспользовалось ботом: {len(activ_us)}\n"
                               f"Передано запросов в бота: {req}\n"
                               f"Пользователей зарегистрировано: {len(users.keys())}")
    req = 0
    activ_us = []


if __name__ == '__main__':
    Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    schedule.every().day.at("03:00").do(updating_mgou)
    schedule.every(3).hours.do(updating)
    schedule.every().day.at("23:00").do(statist)
    while True:
        schedule.run_pending()
        time.sleep(1)
