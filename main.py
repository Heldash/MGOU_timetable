# import datetime
# from openpyxl import load_workbook
# import json
# import io
# import urllib.request
# import re
# import pprint
# # def udate_rasp():
# url = "https://docs.google.com/spreadsheets/d/1hJ6DmaxRVx2TQVCVsG_Sa-vdD0-d4chd/edit#gid=317033260/export?format=csv"
# resp = urllib.request.urlopen(url)
# with io.TextIOWrapper(resp, encoding='utf-8') as f:
# # wb = load_workbook("./40_03_01_Правозащитная_деятельность_с_интенсивным_изучением_иностранного.xlsx")
#     wb = load_workbook(f)
# sheet = wb['Лист1']
# print(sheet.max_row, sheet.max_column)
# date_pars = {}
# for i in range(3,sheet.max_row):
#     res = sheet.cell(row=i, column=1).value
#     # print(type(res))
#     if type(res) == datetime.datetime:
#         day = res.strftime("%d.%m.%y")
#         date_pars[day] = [[]]*7
#         for k in range(i,i+7):
#             date_pars[day][k-i] = sheet.cell(row=k, column=7).value
# pdsi= {"ПДСИИЯ":[]}
# data = {}
# for i in date_pars:
#     data[i] ={
#         "1 pars": date_pars[i][0],
#         "2 pars": date_pars[i][1],
#         "3 pars": date_pars[i][2],
#         "4 pars": date_pars[i][3],
#         "5 pars": date_pars[i][4],
#         "6 pars": date_pars[i][5],
#         "7 pars": date_pars[i][6]}
# pdsi["ПДСИИЯ"].append(data)
#
# with open("ПДСИИЯ_t.json","w") as write_file:
#     json.dump(pdsi,write_file,indent= 2,ensure_ascii=False)
# # with open("ПДСИИЯ.json","r") as read_file:
# #     f = json.load(read_file)
# #     print(f)
# #     s = json.load(read_file)
# #     g = json.dumps(s,indent= 3)
# #     print(g)
# # for i in date_pars:
# #     print(i)
# #     cnt = 1
# #     for k in date_pars[i]:
# #         print(cnt, k)
# #         cnt +=1
# # for i in range(3,sheet.max_row):
# #     par = sheet.cell

names_napr = ["44.03.05 Педагогическое образование География и иностранный (английский) язык",
              "44.03.05 Педагогическое образование География и русский язык как иностранный",
              "44.03.05 Педагогическое образование География и экономическое образование",
              "44.03.05 Педагогическое образование Биология и химия",
              "05.03.06 Экология и природопользование Геоэкология",
              "06.03.01 Биология Биомедицинские технологии",
              "06.03.01 Биология Биоэкология"]
title = "Расписание занятий обучающихся факультета естественных наук очной формы обучения по направлению подготовки 44.03.05 Педагогическое образование, профиль: География и экономическое образование на 1, 3, 5, 7, 9  семестры 2022-2023 учебного года "
flag = True
for name in names_napr:
    if all(i in title for i in name.split()):
        actual_group = name
        print(actual_group)