# # -*- coding: cp1251 -*-
import requests
import telebot
from bs4 import BeautifulSoup as bs
import json
import telebot
def up_mgou(mgou,bot:telebot.TeleBot):
    url= "https://old.mgou.ru/tablitsa-raspianiya-2021-1/"
    r = requests.get(url)
    soup = bs(r.text,"lxml")
    tire = list(soup.find_all("td"))
    # print(type(list(tire)))
    fak = {}
    fakult = ""
    isdis = False
    i = 0
    bmc= ozo = ""
    while i < len(tire):
        res = tire[i] #Здесь берем 1 яйчейку таблицы
        print(res)
        if "Факультет" in res.text or "факультет" in res.text:
            isdis = False
            fak[res.text]={"Очная":{"Бакалавр":{},"Магистр":{},"Специалитет":{}},
                                "Заочная":{"Бакалавр":{},"Магистр":{},"Специалитет":{}},
                                "Очно-заочная":{"Бакалавр":{},"Магистр":{},"Специалитет":{}}}
            fakult = res.text
        elif res.text in ("Очная","Заочная","Очно-заочная"):
            isdis =True
            ozo = res.text #Очная заочная очн-заочн
        elif isdis and res.text in("Бакалавр","Магистр","Специалист","Специалитет"):
            if res.text in("Специалитет","Специалист"):
                bmc = "Специалитет" #Специалитет
                napr = str(tire[i+1].text+" "+tire[i+2].text)
                fak[fakult][ozo][bmc][napr] = []
                i+=3
                continue
            else:
                bmc = res.text #бакалавр или магистр
                napr = str(tire[i + 1].text + " " + tire[i + 2].text)
                fak[fakult][ozo][bmc][napr] = []
                i += 3
                continue
        elif res.find_all("a") != None:
                for j in res.find_all("a"):
                    fak[fakult][ozo][bmc][napr].append(j["href"])
        i+=1

    for i in fak.copy():
        for k in fak[i].copy():
            for j in fak[i][k].copy():
                if fak[i][k][j] == {}:
                    del fak[i][k][j]
            if fak[i][k] == {}:
                del fak[i][k]
    if fak != {}:
        bot.send_message(437194156,"Данные удачно собраны с сайта)")
        with open("mgou.json","w") as file:
            json.dump(fak,file,indent= 3,ensure_ascii=True)
        return fak
    else:
        bot.send_message(437194156,"Не удалось забрать данные с сайта")
        return mgou

def proff_parsing():
    url = "https://guppros.ru/sveden/employees"
    req = requests.get(url)
    soup = bs(req.text, "lxml")
    # print(req.text)
    fio_arr = soup.find_all(itemprop="fio")
    fio = []
    for i in fio_arr:
        fio.append(i.text)
    res = []
    if fio:
        for k in fio:
            inicial = k.split()
            if (len(inicial) == 2):
                res.append(f"{inicial[0]} {(inicial[1])[0]}.")
                res.append(f"{inicial[0]}{(inicial[1])[0]}.")
            elif(len(inicial) == 3):
                res.append(f"{inicial[0]} {(inicial[1])[0]}.{(inicial[2])[0]}.")
                res.append(f"{inicial[0]}{(inicial[1])[0]}.{(inicial[2])[0]}.")
    if res:
        res = set(res)
        res = sorted(res)
        with open("proffesors.json","w") as file:
            json.dump(res,file,indent= 3)

    # return res
if __name__ == "__main__":
    up_mgou()
    proff_parsing()
# proff_parsing()
# with open("proffesors.json","r") as file:
#     arr = json.load(file)
#     print(len(sorted(set(arr))))