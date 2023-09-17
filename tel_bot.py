import os

import telebot
import datetime
import json
import re
import random
from GoogleShetrob import update
from raspisanie_update import upload_rasp
import TOKEN
# import time


# token = "5825628945:AAGZ1pDqtBYxLLA3yAfmYVsT98wmeeV5Ja4"
# token2 = "1512279847:AAF5MKawMcFwjx7khpVAJgdysUEDe9LvBsk"
token  = TOKEN.TOKEN1
bot = telebot.TeleBot(token)
comm = ['start','Расписание на сегодня',"Расписание на завтра","Календарь","Сменить группу",
                               "Информация и обратная связь"]
# bot.get_my_commands()
stik_ran = ["CAACAgQAAxkBAAEGn9Bjh0tp3dzMwK5JO1BvSVI0yCUsAQACOw0AAtbmSFAxK-1eG55cfCsE",
            "CAACAgEAAxkBAAEGn9Rjh0z1rnIVn85ZVPXa9DZBUnkFLgACawQAAvhi8ERmUaTo2t1t_ysE",
            "CAACAgIAAxkBAAEGn9Zjh01Aw8ick5OeDUs06WTWJYcdQAACXAEAAhAabSKcIs6F61GChSsE",
            "CAACAgQAAxkBAAEGn9hjh04AAXlITxIq_Jaz10xVdTlyuH4AAkMLAALo4aBSIDcpNsGm758rBA",
            "CAACAgIAAxkBAAEGomVjiHEw3k0rKIbKRjjtmCYg06xAhQAC0RsAAhyGcUjQ7Rs7CfNrAysE",
            "CAACAgEAAxkBAAEGomdjiHSYhtzKYOODjoS-_0l60dh74QACnAIAAtscqEdAo37j6Iyu8CsE"]
month = ["Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Авгус","Сентябрь","Октябрь","Ноябрь","Декабрь"]
wday= ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]
with open("mgou.json","r") as file:
    rasp_mgou = json.load(file)
with open("Users.json","r") as file:
    try:
        users = json.load(file)
    except:
        users = {}
osn_dir = os.getcwd()
abrev = {'Факультет безопасности жизнедеятельности':'OBZ',
'Факультет естественных наук':'SIEN',
'Факультет изобразительного искусства и народных ремёсел':'IMAG',
'Факультет истории, политологии и права':'HPP',
'Лингвистический факультет':'LINGV',
'Факультет психологии':'PSYH',
'Факультет романо-германских языков':'RGLANG',
'Факультет русской филологии':'RFIL',
'Факультет специальной педагогики и психологии':'SOCPED',
'Физико-математический факультет':'PHYS',
'Факультет физической культуры':'FIZK',
'Экономический факультет':'ECONOM',
'Юридический факультет':'YRID',
'Медицинский факультет':'MED',}

abrev_rash={'OBZ':'Факультет безопасности жизнедеятельности',
'SIEN':'Факультет естественных наук',
'IMAG':'Факультет изобразительного искусства и народных ремёсел',
'HPP':'Факультет истории, политологии и права',
'LINGV':'Лингвистический факультет',
'PSYH':'Факультет психологии',
'RGLANG':'Факультет романо-германских языков',
'RFIL':'Факультет русской филологии',
'SOCPED':'Факультет специальной педагогики и психологии',
'PHYS':'Физико-математический факультет',
'FIZK':'Факультет физической культуры',
'ECONOM':'Экономический факультет',
'YRID':'Юридический факультет',
'MED':'Медицинский факультет',}

mark_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = telebot.types.KeyboardButton("Расписание на сегодня")
btn2 = telebot.types.KeyboardButton("Расписание на завтра")
btn3 = telebot.types.KeyboardButton("Календарь")
btn4 = telebot.types.KeyboardButton("Календарь факультативов")
btn5 = telebot.types.KeyboardButton("Сменить группу")
btn6 = telebot.types.KeyboardButton("Информация и обратная связь")
btn7 = telebot.types.KeyboardButton("Пожертвование")
mark_menu.add(btn1,btn2)
mark_menu.add(btn3,btn4)
mark_menu.add(btn5)
mark_menu.add(btn6)
mark_menu.add(btn7)


#Начало формы регистрации
def create_inline_keyboard_forFak():
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    fak = [i for i in rasp_mgou]
    # print(type(fak[0]))
    # print(fak)
    for k in fak:
        # print(k)
        btn = telebot.types.InlineKeyboardButton(k.lower().replace("факультет",""),callback_data=f"fak{abrev[k]}")
        markup.add(btn)
    return markup


def create_form_ob(fak):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for i in rasp_mgou[fak]:
        btn = telebot.types.InlineKeyboardButton(i,callback_data=f"rez{i}")
        markup.add(btn)
    naz = telebot.types.InlineKeyboardButton("Назад",callback_data="nazfak")
    markup.add(naz)
    return markup
def create_level(fak,form):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for i in rasp_mgou[fak][form]:
        btn = telebot.types.InlineKeyboardButton(i,callback_data=f"bms{i}")
        markup.add(btn)
    naz = telebot.types.InlineKeyboardButton("Назад",callback_data="nazrez")
    markup.add(naz)
    return markup
def create_kod(fak,form,level):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    with open(os.path.join(os.getcwd(),"Fakultet",fak,form,level,"group.json"),"r")as file_gr:
        kod = json.load(file_gr)
        kod = kod["расшифровка"]
    for i in kod:
        # btn = telebot.types.InlineKeyboardButton(kod[i], callback_data=f"kod{i}")
        btn = telebot.types.KeyboardButton(i)
        # print(i)
        markup.add(btn)
    naz = telebot.types.KeyboardButton("Назад")
    markup.add(naz)
    return markup
#Конец формы регистрации


def create_group(fak,form,level,kod):
    with open(f"./Fakultet/{fak}/{form}/{level}/group.json","r") as gr:
        groups = json.load(gr)
        key_words = groups['расшифровка']
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        array_groups = list(groups[key_words[kod]]["Учебные дисциплины"]["Занятия"].keys())
        # for vector in groups:
        #     if vector != 'расшифровка':
        # for stud_ftd in groups[key_words[kod]]:
        #     for view in groups[key_words[kod]][stud_ftd]:
        #         if groups[key_words[kod]][stud_ftd][view] != {}:
        #             array_groups += list(groups[key_words[kod]][stud_ftd][view].keys())

        # array_groups = set(array_groups)
        # array_groups = list(groups[key_words[kod]]["Учебные дисциплины"]["Занятия"].keys())
        for i in array_groups:
            btn = telebot.types.KeyboardButton(i)
            markup.add(btn)
        # naz = telebot.types.InlineKeyboardButton("Назад", callback_data="naz")
        naz = telebot.types.InlineKeyboardButton("Назад", callback_data="nazkod")
        markup.add(naz)
        return markup
def open_timetable(user):
    """Возвращает словарь с расписанием группы, на вход функции поступает масиив данных пользователя"""
    with open(os.path.join("./Fakultet",user[0],user[1],user[2],"group.json"),"r") as file:
        timetable = json.load(file)
        naprav = timetable["расшифровка"][user[3]]
        return timetable[naprav]
def op_json_for_user(mes_id):
    """Возвращает массив с данными пользователя
    user[0] - Факультет
    user[1] - Форма обучения
    user[2] - Уровень образования
    user[3] - аббревиатура направления
    user[4] - группа
    user[5] - факультатив"""
    with open("Users.json", "r") as file:
        try:
            user = json.load(file)
        except:
            user = None
        if str(mes_id) in user:
            return user[str(mes_id)]
        else:
            bot.send_message(mes_id,"Вы не выбрали не одну группу пожалуйста нажмите на кнопку "
                                    "'Сменить группу' или введите команду '\\start'")
@bot.message_handler(commands=['start'])
def start_message(message):
    """Настройка пользователя"""
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("Обновить расписание")
    btn2 = telebot.types.KeyboardButton("Расписание на сегодня")
    btn3 = telebot.types.KeyboardButton("Расписание на завтра")
    btn4 = telebot.types.KeyboardButton("Календарь")
    btn5 = telebot.types.KeyboardButton("Сменить группу")
    btn6 = telebot.types.KeyboardButton("Информация и обратная связь")
    markup.add(btn1,btn2,btn3)
    markup.add(btn4)
    markup.add(btn5)
    markup.add(btn6)
    # with open("Users.json", "w") as us:
    #     users = json.load(us)
    # global user_id
    # global user
    bot.send_message(message.chat.id,"Здравствуй дорогой студент, если вдруг вы ошиблись при выборе в чем то введите еще раз"
                                     "комманду '\\start' или нажмите на кнопку 'Сменить группу'",reply_markup=markup)
    users[str(message.chat.id)] = ["_"]*6
    WELCOME_text = "Я бот и был создан для решения вопроса с рассписанием\n" \
                   "На данный момент я умею пока что показывать рассписание пар\n" \
                   "Пока что недоступно расписание зачетных и экзаменационных сессий\n" \
                   "Для начала работы пожалуйств выберете ваш факультет"
    bot.send_message(message.chat.id, WELCOME_text, reply_markup=create_inline_keyboard_forFak())

    mark = telebot.types.InlineKeyboardMarkup(row_width=2)
    mark.add(telebot.types.InlineKeyboardButton("Календарь", callback_data="&calendar"))
    zav = telebot.types.InlineKeyboardButton("Расписание на завтра", callback_data="Zav")
    seg = telebot.types.InlineKeyboardButton("Рассписание на сегодня", callback_data="Seg")
    mark.add(seg, zav)
    # bot.send_message(message.chat.id,"Здесь должна быть ваша реклама",reply_markup=markup)
    # bot.send_message(message.chat.id,"Ну а теперь можете выбрать дату используя кнопки находящиееся внизу в меню или под этим сообщением",reply_markup=mark)

# start - запускает выбор направления и группы
# today - Показывает расписание занятий на сегодняшний день
# tomorrow - Показывает расписаний занятий на завтра
# calendar - Выводит календарь, в котором можно будет выбрать дату, на которую нужно узнать расписание
# change_group - Запускает выбор направления и группы
# information - Выдает информацию об авторе и контакты для связи с разработчиком
@bot.message_handler(commands=["today","today","tomorrow","calendar","change_group","information","update","donat","calendar_ftd"])
def other_commands(message):
    if message.text == "/today":
        ass = datetime.datetime.now()  # Дата сегодняшняя если что)
        res = ass.strftime("%d.%m.%y")
        mark = telebot.types.InlineKeyboardMarkup(row_width=2)
        mark.add(telebot.types.InlineKeyboardButton("Календарь", callback_data="&calendar"))
        zav = telebot.types.InlineKeyboardButton("Расписание на завтра", callback_data="Zav")
        seg = telebot.types.InlineKeyboardButton("Рассписание на сегодня", callback_data="Seg")
        mark.add(seg, zav)
        bot.send_message(message.chat.id, but_rasp(res, message.chat.id), reply_markup=mark)
    elif message.text == "/tomorrow":
        aft = datetime.datetime.now()
        aft = aft + datetime.timedelta(days=1)
        zav = aft.strftime("%d.%m.%y")
        mark = telebot.types.InlineKeyboardMarkup(row_width=2)
        mark.add(telebot.types.InlineKeyboardButton("Календарь", callback_data="&calendar"))
        zavtr = telebot.types.InlineKeyboardButton("Расписание на завтра", callback_data="Zav")
        seg = telebot.types.InlineKeyboardButton("Рассписание на сегодня", callback_data="Seg")
        mark.add(seg, zavtr)
        bot.send_message(message.chat.id, but_rasp(zav, message.chat.id), reply_markup=mark)
    elif message.text == "/calendar":
        dat = datetime.datetime.now().timetuple()
        year = dat.tm_year
        mes = dat.tm_mon
        bot.send_message(message.chat.id, "Выберете дату", reply_markup=calendar(mes, year, message.chat.id))
    elif message.text == "/change_group":
        users[str(message.chat.id)] = ["_"] * 6
        bot.send_message(message.chat.id, "Выберите факультет: ", reply_markup=create_inline_keyboard_forFak())
    elif message.text == "/information":
        bot.send_message(message.chat.id, "Мои создатель Игорь Смирнов такой же студент как и вы 😜\n"
                                          "Ссылки на соц сети и обратную связь с разработчиком\n"
                                          "-------------------------------------------------\n"
                                          "<b>Почта</b>✉: dartin.rok@yandex.ru \n"
                                          "<b>VK</b>✌: <a href='https://vk.com/ygoryochek'>ygoryochek</a>\n"
                                          "<b>Телеграм</b>🤙: <a href='https://t.me/ygoryochek'>Ссылка</a>\n"
                                          "<b>GitHub</b>:<a href='https://github.com/Heldash'>Heldash</a>"
                                          "-------------------------------------------------\n"
                                          "💵💵Также буду рад если поддержите меня денюжкой💵💵\n"
                                          "<strong>Сбер</strong>💰: 4276400102891869", parse_mode="HTML",
                         disable_web_page_preview=True)
    elif message.text == "/donate":
        bot.send_message(message.chat.id,"Эти пожертвования помогут с развитием и поддержкой в работе бота"
                                         "💰<strong>Сбер</strong>💰: 4276400102891869", parse_mode="HTML",
                         disable_web_page_preview=True)
    elif message.text == "/update":
        if str(message.chat.id) != "437194156":
            bot.send_message(message.chat.id,"Разработчик оставил эту команду для себя но вы ее не трогайте :)")
        elif str(message.chat.id) == "437194156":
            bot.send_message(message.chat.id,"Начал обнову")
            bot.send_message(message.chat.id,"Обновляю базу рассписаний")
            update()
            # while not itog:
            #     time.sleep(60)
            #     itog = update()
            bot.send_message(message.chat.id, "Загружаю рассписвние групп")
            upload_rasp()
            bot.send_message(message.chat.id, "Загрузка произошла успешно")
            os.chdir(osn_dir)
    elif message.text == "/calendar_ftd":
        mark = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        user = op_json_for_user(message.chat.id)
        timetable = open_timetable(user)
        group = []
        for ezg in timetable["ФТД"]:
            if timetable['ФТД'][ezg] != {}:
                group+= list(timetable["ФТД"][ezg].keys())
        group = set(group)
        if users[str(message.chat.id)][5] == "_":
            if any(timetable["ФТД"][i] != {} for i in timetable["ФТД"]):
                for i in group:
                    mark.add(telebot.types.KeyboardButton(i))
                    # group[i] = telebot.types.KeyboardButton(group[i])
                mark.add(telebot.types.KeyboardButton("Назад"))
                send = bot.send_message(message.chat.id,"Выберите из кнопок ниже группу по факультативам, если хотите прекратить выбор нажмите отмена: ",reply_markup=mark)
                bot.register_next_step_handler(send, views_groups)
            else:
                bot.send_message(message.chat.id,"В вашей группе нет факультативов")
        else:
            if user[5] in group:
                dat = datetime.datetime.now()
                dat = dat.timetuple()
                bot.send_message(message.chat.id,"Выберите дату: ",reply_markup=calendar_ftd(dat.tm_year,dat.tm_mon,
                                                                                             str(message.chat.id)))

def views_groups(message):
    groups = open_timetable(users[str(message.chat.id)])
    gr = []
    for i in groups["ФТД"]:
        gr+= groups["ФТД"][i].keys()
    gr = set(gr)
    if message.text in gr:
        dat = datetime.datetime.now()
        dat = dat.timetuple()
        users[str(message.chat.id)][5] = message.text
        with open("Users.json","r") as file:
            try:
                all_user = json.load(file)
            except:
                all_user = {}
        with open("Users.json","w") as f:
            if str(message.chat.id) in all_user:
                del all_user[str(message.chat.id)]
                json.dump(users,f,indent=2, ensure_ascii=False)
            else:
                json.dump(users, f, indent=2, ensure_ascii=False)
        bot.send_message(message.chat.id,f"Вы выбрали: {message.text}",reply_markup= mark_menu)
        bot.send_message(message.chat.id, "Выберите дату: ",reply_markup=calendar_ftd(dat.tm_year,dat.tm_mon,str(message.chat.id)))
    elif message.text == "Отмена":
        bot.send_message(message.chat.id, "Действие отменено")
    else:
        send = bot.send_message(message.chat.id,"К сожалению такого факультета не существует")
        bot.register_next_step_handler(send, views_groups)

def calendar_ftd(year,mes,mes_id):
    """"""
    us = users[str(mes_id)][5]
    markup1 = telebot.types.InlineKeyboardMarkup(row_width=7)
    markup1.add(telebot.types.InlineKeyboardButton(us,callback_data="_"))
    title = telebot.types.InlineKeyboardButton(year, callback_data="_")
    markup1.add(title)
    wd1 = telebot.types.InlineKeyboardButton("Пн", callback_data="_")
    wd2 = telebot.types.InlineKeyboardButton("Вт", callback_data="_")
    wd3 = telebot.types.InlineKeyboardButton("Ср", callback_data="_")
    wd4 = telebot.types.InlineKeyboardButton("Чт", callback_data="_")
    wd5 = telebot.types.InlineKeyboardButton("Пт", callback_data="_")
    wd6 = telebot.types.InlineKeyboardButton("Сб", callback_data="_")
    markup1.add(wd1, wd2, wd3, wd4, wd5, wd6)
    mass = ["_"] * 6
    for i in range(1, 32):
        try:
            dat = datetime.date(year, mes, i)
        except:
            if any(i!="_" for i in mass):
                days_arr = []
                for k in mass:
                    days_arr.append(obj_creat(k, year, mes, mes_id, True, us))
                markup1.add(days_arr[0],days_arr[1],days_arr[2],days_arr[3],days_arr[4],days_arr[5])
            break
        inf = dat.timetuple()
        if inf.tm_wday < 6:
            mass[inf.tm_wday] = i
        if inf.tm_wday == 5:
            days_arr = []
            for i in mass:
                days_arr.append(obj_creat(i, year, mes, mes_id, True, us))
                    # days_arr.append(telebot.types.InlineKeyboardButton(
                    #     check_lesson(op_json_for_user(call.message.message_id), group, "ФТД"
                    #                  , datetime.date(year, mes, i), i),
                    #     callback_data=str(f"ftd.{dat.strftime('%d.%m.%y')}")))
            # markup1.add(obj_creat(mass[0], year, mes,mes_id), obj_creat(mass[1], year, mes,mes_id), obj_creat(mass[2], year, mes,mes_id),
            #             obj_creat(mass[3], year, mes,mes_id), obj_creat(mass[4], year, mes,mes_id), obj_creat(mass[5], year, mes,mes_id))
            markup1.add(days_arr[0],days_arr[1],days_arr[2],days_arr[3],days_arr[4],days_arr[5])
            mass = ["_"] * 6
    else:
        if any(i != "_" for i in mass):
            days_arr = []
            for k in mass:
                days_arr.append(obj_creat(k, year, mes, mes_id, True, us))
            markup1.add(days_arr[0],days_arr[1],days_arr[2],days_arr[3],days_arr[4],days_arr[5])
    nalev = telebot.types.InlineKeyboardButton("<=", callback_data=f"ftd.<.{mes}.{year}")
    mesyac = telebot.types.InlineKeyboardButton(month[inf.tm_mon - 1], callback_data="ftd.month")
    napravo = telebot.types.InlineKeyboardButton("=>", callback_data=f"ftd.>.{mes}.{year}")
    markup1.add(nalev, mesyac, napravo)
    zav = telebot.types.InlineKeyboardButton("Расписание на завтра", callback_data="ftd.Zav")
    seg = telebot.types.InlineKeyboardButton("Рассписание на сегодня", callback_data="ftd.Seg")
    markup1.add(seg, zav)
    return markup1


@bot.callback_query_handler(lambda call: call.data[:3]=="")



@bot.message_handler(content_types=['text'])
def osnova(message):
    if message.text == "Расписание на сегодня":
        ass = datetime.datetime.now() #Дата сегодняшняя если что)
        res = ass.strftime("%d.%m.%y")
        mark = telebot.types.InlineKeyboardMarkup(row_width=2)
        mark.add(telebot.types.InlineKeyboardButton("Календарь", callback_data="&calendar"))
        zav = telebot.types.InlineKeyboardButton("Расписание на завтра", callback_data="Zav")
        seg = telebot.types.InlineKeyboardButton("Рассписание на сегодня", callback_data="Seg")
        mark.add(seg, zav)
        bot.send_message(message.chat.id,but_rasp(res,message.chat.id),reply_markup=mark)


    elif message.text == "Расписание на завтра":
        aft= datetime.datetime.now()
        aft =  aft + datetime.timedelta(days=1)
        zav = aft.strftime("%d.%m.%y")
        mark = telebot.types.InlineKeyboardMarkup(row_width=2)
        mark.add(telebot.types.InlineKeyboardButton("Календарь", callback_data="&calendar"))
        zavtr = telebot.types.InlineKeyboardButton("Расписание на завтра", callback_data="Zav")
        seg = telebot.types.InlineKeyboardButton("Рассписание на сегодня", callback_data="Seg")
        mark.add(seg, zavtr)
        bot.send_message(message.chat.id,but_rasp(zav, message.chat.id),reply_markup=mark)


    elif message.text == "Обновить расписание":
        if str(message.chat.id) != "437194156":
            bot.send_message(message.chat.id,"Разработчик пока что оставил эту кнопку но вы ее не трогайте :)")
        elif str(message.chat.id) == "437194156":
            bot.send_message(message.chat.id,"Начал обнову")
            bot.send_message(message.chat.id,"Обновляю базу рассписаний")
            update()
            bot.send_message(message.chat.id, "Загружаю рассписвние групп")
            upload_rasp()
            bot.send_message(message.chat.id, "Загрузка произошла успешно")
            os.chdir(osn_dir)


    elif re.fullmatch(r"\d\d\D\d\d\D\d\d",message.text):
        dat = message.text[0:2]+"."+message.text[3:5]+"."+message.text[6:8]
        bot.send_message(message.chat.id,but_rasp(dat,message.chat.id))


    elif message.text == "Календарь":
        dat = datetime.datetime.now().timetuple()
        year = dat.tm_year
        mes = dat.tm_mon
        bot.send_message(message.chat.id,"Выберете дату",reply_markup=calendar(mes,year,message.chat.id))


    elif message.text == "Сменить группу":
        users[str(message.chat.id)] = ["_"]*6
        bot.send_message(message.chat.id, "Выберите факультет: ", reply_markup=create_inline_keyboard_forFak())
        # User(message.chat.id)
        # bot.send_message(message.chat.id,"Пока что не работает")


    elif message.text == "Информация и обратная связь":
        bot.send_message(message.chat.id,"Мои создатель Игорь Смирнов такой же студент как и вы 😜\n"
                                          "Ссылки на соц сети и обратную связь с разработчиком\n"
                                          "-------------------------------------------------\n"
                                          "<b>Почта</b>✉: dartin.rok@yandex.ru \n"
                                          "<b>VK</b>✌: <a href='https://vk.com/ygoryochek'>ygoryochek</a>\n"
                                          "<b>Телеграм</b>🤙: <a href='https://t.me/ygoryochek'>Ссылка</a>\n"
                                          "<b>GitHub</b>:<a href='https://github.com/Heldash'>Heldash</a>"
                                          "-------------------------------------------------\n"
                                          "💵💵Также буду рад если поддержите меня денюжкой💵💵\n"
                                          "<strong>Сбер</strong>💰: 4276400102891869", parse_mode="HTML",
                         disable_web_page_preview = True)
    else:
        bot.send_message(message.chat.id,"К сожалению, я не знаю что это")
        bot.send_sticker(message.chat.id,stik_ran[random.randint(0,len(stik_ran)-1)])

@bot.callback_query_handler(func=lambda call: call.data[:3] in ("fak","rez","bms","kod","naz","gro"))
def user_add(call):
    if call.data[:3]=="fak":
        info = call.data[3:]
        info = abrev_rash[info]
        users[str(call.message.chat.id)][0] = info
        bot.edit_message_text("Выберите форму обучения:",chat_id=str(call.message.chat.id),
                              message_id=call.message.message_id,
                              reply_markup=create_form_ob(info))
        # user.add_fakult(info,call.message.message_id)
    elif call.data[:3]=="rez":
        info = call.data[3:]
        users[str(call.message.chat.id)][1] = info
        bot.edit_message_text("Уровень обучения:", chat_id=str(call.message.chat.id),
                              message_id=call.message.message_id,
                              reply_markup=create_level(users[str(call.message.chat.id)][0],info))
        # user.add_form(info, call.message.message_id)
    elif call.data[:3]=="bms":
        info = call.data[3:]
        users[str(call.message.chat.id)][2] = info
        bot.edit_message_text("Выберите форму обучения:", chat_id=str(call.message.chat.id),
                              message_id=call.message.message_id,
                              reply_markup=create_kod(users[str(call.message.chat.id)][0],
                              users[str(call.message.chat.id)][1],info))
        # user.add_level(info, call.message.message_id)
    elif call.data[:3]=="kod":
        info = call.data[3:]
        users[str(call.message.chat.id)][3] = info
        send = bot.edit_message_text("Выберите направление:", chat_id=str(call.message.chat.id),
                              message_id=call.message.message_id,
                              reply_markup=create_group(users[str(call.message.chat.id)][0],
                                                      users[str(call.message.chat.id)][1],
                                                        users[str(call.message.chat.id)][2],
                                                      info))
        bot.register_next_step_handler(send, views_groups)
        # user.add_kod(info, call.message.message_id)
    elif call.data[:3]=="gro":
        with open(os.path.join(os.getcwd(),"Fakultet",users[str(call.message.chat.id)][0],
                               users[str(call.message.chat.id)][1],users[str(call.message.chat.id)][2],
                               "group.json"),"r") as file_kods:
            kod = json.load(file_kods)
            kod = kod["расшифровка"]#Загружаю коды расшифровки направлений
        info = call.data[3:]
        users[str(call.message.chat.id)][4] = info
        bot.edit_message_text(f"Вы выбрали {users[str(call.message.chat.id)][0]} "
                              f"\nФорму обучения:{users[str(call.message.chat.id)][1]}"
                              f"\nУровень обучения: {users[str(call.message.chat.id)][2]}"
                              f"\nКод программы: {kod[users[str(call.message.chat.id)][3]]}"
                              f"\nГруппу: {users[str(call.message.chat.id)][4]}",
                              chat_id=str(call.message.chat.id),
                              message_id=call.message.message_id,
                              reply_markup=None)
        with open("Users.json","r") as file:
            try:
                all_user = json.load(file)
            except:
                all_user = {}
        with open("Users.json","w") as f:
            if str(call.message.chat.id) in all_user:
                del all_user[str(call.message.chat.id)]
                json.dump(users,f,indent=2, ensure_ascii=False)
            else:
                json.dump(users, f, indent=2, ensure_ascii=False)
        # user.add_user(info, call.message.message_id)
    elif call.data[:3]== "naz":
        info = call.data[3:]
        if info == "fak":# Назад к выбору факультета
            bot.edit_message_text("Выберете факультет:",chat_id=str(call.message.chat.id),
                              message_id=call.message.message_id,
                              reply_markup=create_inline_keyboard_forFak())
        elif info == "rez":# Назад к выбору формы обучения
            bot.edit_message_text("Выберите форму обучения:",chat_id=str(call.message.chat.id),
                              message_id=call.message.message_id,
                              reply_markup=create_form_ob(users[str(call.message.chat.id)][0]))
        elif info == "bms":# Назад к выбору уровня
            bot.edit_message_text("Выберите уровень:",chat_id=str(call.message.chat.id),
                              message_id=call.message.message_id,
                              reply_markup=create_level(users[str(call.message.chat.id)][0],
                                                        users[str(call.message.chat.id)][1]))
        elif info == "kod":# Назад к коду программы
            bot.edit_message_text("Выберите код:",chat_id=str(call.message.chat.id),
                              message_id=call.message.message_id,
                              reply_markup=create_kod(users[str(call.message.chat.id)][0],
                                                      users[str(call.message.chat.id)][1],
                                                      users[str(call.message.chat.id)][2]))
    
@bot.callback_query_handler(func=lambda call:re.fullmatch(r"\d\d\D\d\d\D\d\d",call.data))
def day_call(call):
    mark = telebot.types.InlineKeyboardMarkup(row_width=2)
    mark.add(telebot.types.InlineKeyboardButton("Календарь", callback_data="&calendar"))
    zav = telebot.types.InlineKeyboardButton("Расписание на завтра", callback_data="Zav")
    seg = telebot.types.InlineKeyboardButton("Рассписание на сегодня", callback_data="Seg")
    mark.add(seg, zav)
    bot.edit_message_text(chat_id=str(call.message.chat.id), message_id=call.message.message_id,
                          text=but_rasp(call.data, str(call.message.chat.id)), reply_markup=mark)

@bot.callback_query_handler(func=lambda call: call.data[0]in"<>!&" or call.data == "month" or call.data in
                                              ("Seg","Zav"))
def kalendar_call(call):
    """Взаимодействует с календарем учебных занятий"""
    try:
        if call.message:
            mark = telebot.types.InlineKeyboardMarkup(row_width=2)
            mark.add(telebot.types.InlineKeyboardButton("Календарь", callback_data="&calendar"))
            zav = telebot.types.InlineKeyboardButton("Расписание на завтра", callback_data="Zav")
            seg = telebot.types.InlineKeyboardButton("Рассписание на сегодня", callback_data="Seg")
            mark.add(seg, zav)
            dat = datetime.datetime.now().timetuple()
            if dat.tm_mon <=7:
                period = (dat.tm_year-1,dat.tm_year)
            else:
                period = (dat.tm_year,dat.tm_year+1)
            if call.data[0] == "<":
                mes,year = map(int,call.data.split(".")[1:])
                mes -= 1
                if mes<=0:
                    year-=1
                    mes = 12
                if mes >7 and year==period[0] or mes<=7 and year == period[1]:
                    bot.edit_message_text(chat_id=str(call.message.chat.id), message_id=call.message.message_id,
                                          text="Выберете дату:", reply_markup=calendar(mes, year,str(call.message.chat.id)))
                else:
                    bot.answer_callback_query(call.message.message_id,show_alert=False,text="Дальше нельзя")
                    # bot.answer_callback_query(str(call.message.chat.id),show_alert=False,text="Дальше нельзя")
                    # bot.send_message(str(call.message.chat.id),"Дальше нельзя)")
                # bot.edit_message_text(chat_id=str(call.message.chat.id),message_id=call.message.message_id,text="Выберете дату",reply_markup=calendar(mes,year))
            elif call.data[0] == ">":
                mes, year = map(int,call.data.split(".")[1:])
                mes += 1
                if mes > 12:
                    year += 1
                    mes = 1
                # if mes < 7 and year>dat.tm_year or mes<=7 and year == dat.tm_year:
                if mes >7 and year==period[0] or mes<=7 and year == period[1]:
                    bot.edit_message_text(chat_id=str(call.message.chat.id), message_id=call.message.message_id,
                                          text="Выберете дату:", reply_markup=calendar(mes, year,str(call.message.chat.id)))
                else:
                    bot.answer_callback_query(call.message.message_id, show_alert=False, text="Дальше нельзя")
                    # bot.answer_callback_query(callback_query_id=str(call.message.chat.id), show_alert=False, text="Дальше нельзя")
                    # bot.send_message(str(call.message.chat.id),"Дальше нельзя)")
            elif call.data[:5] == "month":
                bot.edit_message_text(chat_id=str(call.message.chat.id),message_id=call.message.message_id,text="Выберите месяц:",reply_markup=chos_mes())
            elif call.data[0] == "!":
                mes, year = map(int, call.data.split(".")[1:])
                bot.edit_message_text(chat_id=str(call.message.chat.id), message_id=call.message.message_id,
                                      text="Выберете дату:", reply_markup=calendar(mes, year,str(call.message.chat.id)))
            elif call.data[0] == "&":
                mes,year = dat.tm_mon,dat.tm_year
                bot.edit_message_text(chat_id=str(call.message.chat.id), message_id=call.message.message_id,
                                      text="Выберете дату:", reply_markup=calendar(mes, year, str(call.message.chat.id)))
            elif call.data[:3] == "Seg":
                mes, year,day = dat.tm_mon, dat.tm_year,dat.tm_mday
                dato = datetime.datetime(year,mes,day)
                bot.edit_message_text(chat_id=str(call.message.chat.id), message_id=call.message.message_id,
                                      text=but_rasp(dato.strftime("%d.%m.%y"),str(call.message.chat.id)), reply_markup=mark)
            elif call.data[:3] == "Zav":
                mes, year,day = dat.tm_mon, dat.tm_year,dat.tm_mday
                dato = datetime.datetime(year,mes,day) + datetime.timedelta(days=1)
                bot.edit_message_text(chat_id=str(call.message.chat.id), message_id=call.message.message_id,
                                      text=but_rasp(dato.strftime("%d.%m.%y"),str(call.message.chat.id)), reply_markup=mark)
            else:
                bot.send_message(str(call.message.chat.id),"Вы не туда нажали попробуйте еще раз")
    except Exception as e:
        print(repr(e))

def chos_mes():
    """Выпадающий список из месяцев"""
    markup = telebot.types.InlineKeyboardMarkup(row_width=4)
    dat = datetime.datetime.now().timetuple()
    mes = []
    cnt = 0
    for i in range(6,len(month)):
        mes.append(telebot.types.InlineKeyboardButton(month[i],callback_data="!."+str(i+1)+f".{dat.tm_year if 6<dat.tm_mon<=12 else dat.tm_year-1}"))
        # print("!"+str(i)+f".{dat.tm_year if 6<dat.tm_mon<=12 else dat.tm_year-1}")
        cnt+=1
        if cnt >= 4:
            markup.add(mes[0],mes[1],mes[2],mes[3])
            cnt = 0
            mes = []
    for i in range(6):
        mes.append(telebot.types.InlineKeyboardButton(month[i],callback_data="!."+str(i+1)+f".{dat.tm_year if dat.tm_mon<6 else dat.tm_year+1}"))
        # print("!"+str(i) + f".{dat.tm_year if dat.tm_mon < 6 else dat.tm_year + 1}")
        cnt+=1
        if cnt >=4:
            markup.add(mes[0], mes[1], mes[2], mes[3])
            cnt = 0
            mes = []
    return markup

def calendar(mes,year,mes_id):
    markup1 = telebot.types.InlineKeyboardMarkup(row_width=6)
    markup1.add(telebot.types.InlineKeyboardButton(users[str(mes_id)][4],callback_data="_"))
    title = telebot.types.InlineKeyboardButton(str(year),callback_data="_")
    markup1.add(title)
    wd1 = telebot.types.InlineKeyboardButton("Пн", callback_data="_")
    wd2 = telebot.types.InlineKeyboardButton("Вт", callback_data="_")
    wd3 = telebot.types.InlineKeyboardButton("Ср", callback_data="_")
    wd4 = telebot.types.InlineKeyboardButton("Чт", callback_data="_")
    wd5 = telebot.types.InlineKeyboardButton("Пт", callback_data="_")
    wd6 = telebot.types.InlineKeyboardButton("Сб", callback_data="_")
    markup1.add(wd1, wd2, wd3, wd4, wd5, wd6)
    mass = ["_"] * 6
    for i in range(1, 32):
        try:
            dat = datetime.date(year, mes, i)
        except:
            if any(i != "_" for i in mass):
                markup1.add(obj_creat(mass[0], year, mes,mes_id), obj_creat(mass[1], year, mes,mes_id), obj_creat(mass[2], year, mes,mes_id),
                            obj_creat(mass[3], year, mes,mes_id), obj_creat(mass[4], year, mes,mes_id), obj_creat(mass[5], year, mes,mes_id))
            break
        inf = dat.timetuple()
        if inf.tm_wday < 6:
            mass[inf.tm_wday] = i
        if inf.tm_wday == 5:
            markup1.add(obj_creat(mass[0], year, mes,mes_id), obj_creat(mass[1], year, mes,mes_id), obj_creat(mass[2], year, mes,mes_id),
                        obj_creat(mass[3], year, mes,mes_id), obj_creat(mass[4], year, mes,mes_id), obj_creat(mass[5], year, mes,mes_id))
            mass = ["_"] * 6
    else:
        if any(i != "_" for i in mass):
            markup1.add(obj_creat(mass[0], year, mes,mes_id), obj_creat(mass[1], year, mes,mes_id), obj_creat(mass[2], year, mes,mes_id),
                        obj_creat(mass[3], year, mes,mes_id), obj_creat(mass[4], year, mes,mes_id), obj_creat(mass[5], year, mes,mes_id))
    nalev = telebot.types.InlineKeyboardButton("<=", callback_data=f"<.{mes}.{year}")
    mesyac = telebot.types.InlineKeyboardButton(month[inf.tm_mon - 1], callback_data="month")
    napravo = telebot.types.InlineKeyboardButton("=>", callback_data=f">.{mes}.{year}")
    markup1.add(nalev, mesyac, napravo)
    zav = telebot.types.InlineKeyboardButton("Расписание на завтра", callback_data="Zav")
    seg = telebot.types.InlineKeyboardButton("Рассписание на сегодня", callback_data="Seg")
    markup1.add(seg,zav)
    return markup1


def obj_creat(days,year,mes,mes_id,ftd = False, gr :str = None):
    """Нужен для создания инлайновой клавиатуры"""
    if days != "_":
        user = users[str(mes_id)]
        day = datetime.date(year,mes,days)
        day = day.strftime("%d.%m.%y")
        with open(f"./Fakultet/{user[0]}/{user[1]}/{user[2]}/group.json", "r") as read_file:
            rasp = json.load(read_file)
            rasp = rasp[rasp["расшифровка"][user[3]]]
            is_les = False
            # for ftd_ob in rasp:
            if ftd is False:
                for EZG in rasp["Учебные дисциплины"]:  # Занятия, Экзамен, Зачеты, гос экз
                    if user[4] in rasp["Учебные дисциплины"][EZG]:
                        if day in rasp["Учебные дисциплины"][EZG][user[4]]:
                            is_les = True
                            break
                if is_les:
                    return telebot.types.InlineKeyboardButton(f"{days}📖",
                                                              callback_data=
                                                              str("ych"+datetime.date(year, mes, days).strftime("%d.%m.%y")))
                else:
                    return telebot.types.InlineKeyboardButton(str(days), callback_data="_")
            elif ftd and gr is not None:
                for EZG in rasp["ФТД"]:  # Занятия, Экзамен, Зачеты, гос экз
                    if user[4] in rasp["ФТД"][EZG]:
                        if day in rasp["ФТД"][EZG][gr]:
                            is_les = True
                            break
                if is_les:
                    return telebot.types.InlineKeyboardButton(f"{days}📖",
                                                              callback_data=
                                                              str("ftd"+datetime.date(year, mes, days).strftime("%d.%m.%y")+gr))
                else:
                    return telebot.types.InlineKeyboardButton(str(days), callback_data="_")

    else:
        return telebot.types.InlineKeyboardButton(days, callback_data="_")

    #     for i in u
    #     return telebot.types.InlineKeyboardButton(str(days),callback_data=datetime.date(year, mes, days).strftime("%d.%m.%y"))
    # else:
    #     return telebot.types.InlineKeyboardButton(days,callback_data="_")
def but_rasp_ftd(mes,mes_id,gr):
    """Функция выдачи расписания факультативов"""
    mass = mes.split(".")
    dat = mass[1] + "." + mass[2] + "." + mass[3]
    susnya_dat = datetime.datetime.strptime(dat,"%d.%m.%y")
    inf_dat = susnya_dat.timetuple()
    d = inf_dat.tm_mday
    wd = inf_dat.tm_wday
    user = users[str(mes_id)]

    with open(f"./Fakultet/{user[0]}/{user[1]}/{user[2]}/group.json", "r") as read_file:
        flag = False
        rasp = json.load(read_file)
        name_group = rasp["расшифровка"][user[3]]
        name_month = month[inf_dat.tm_mon - 1].lower()
        if name_month in ("март","август"):
            name_month = name_month+"а"
        else:
            name_month = name_month[: -1] + "я"
        itog = f"[{user[4]}]  " + str(d) + " " + name_month + " " + wday[wd].lower() + "\n" + "Факультативы:\n\n"
        lesson = {"Занятия":None,
                          "Экзамены":None,
                          "Зачеты":None}
        is_les = False
        # for ftd_ob in rasp[name_group]:
        for EZG in rasp[name_group]["ФТД"]:# Занятия, Экзамен, Зачеты, гос экз
            if user[4] in rasp[name_group]["ФТД"][EZG]:
                if dat in rasp[name_group]["ФТД"][EZG][gr]:
                    is_les = True
                    lesson["ФТД"][EZG] = rasp[name_group]["ФТД"][EZG][gr][dat]
        if is_les:
            for i in lesson:
                if lesson[i] is not None:
                    itog+=f"{i}\n"
                    for less in lesson[i]:
                        itog += f"{less}\n\n"
            return itog
        else:
            return "В этот день пар нет"


def but_rasp(mes,mes_id):
    """Функция выдачи расписания учебных занятий"""
    mass = mes.split(".")
    dat = mass[1] + "." + mass[2] + "." + mass[3]
    susnya_dat = datetime.datetime.strptime(dat,"%d.%m.%y")
    inf_dat = susnya_dat.timetuple()
    d = inf_dat.tm_mday
    wd = inf_dat.tm_wday
    user = users[str(mes_id)]

    with open(f"./Fakultet/{user[0]}/{user[1]}/{user[2]}/group.json", "r") as read_file:
        flag = False
        rasp = json.load(read_file)
        name_group = rasp["расшифровка"][user[3]]
        name_month = month[inf_dat.tm_mon - 1].lower()
        if name_month in ("март","август"):
            name_month = name_month+"а"
        else:
            name_month = name_month[: -1] + "я"
        itog = f"[{user[4]}]  " + str(d) + " " + name_month + " " + wday[wd].lower() + "\n\n" + "Учебные дисциплины\n"
        lesson = {"Занятия":None,
                          "Экзамены":None,
                          "Зачеты":None}
        is_les = False
        # for ftd_ob in rasp[name_group]:
        for EZG in rasp[name_group]["Учебные дисциплины"]:# Занятия, Экзамен, Зачеты, гос экз
            if user[4] in rasp[name_group]["Учебные дисциплины"][EZG]:
                if dat in rasp[name_group]["Учебные дисциплины"][EZG][user[4]]:
                    is_les = True
                    lesson["Учебные дисциплины"][EZG] = rasp[name_group]["Учебные дисциплины"][EZG][user[4]][dat]
        if is_les:
            for i in lesson:
                if lesson[i] is not None:
                    itog+=f"{i}\n"
                    for less in lesson[i]:
                        itog += f"{less}\n\n"
            return itog
        else:
            return "В этот день пар нет"
            # bot.send_message(mes_id, "В этот день пар нет")
bot.infinity_polling()