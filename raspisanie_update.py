# # -*- coding: cp1251 -*-
import os
import zipfile
from openpyxl import load_workbook
import json
import datetime
import copy
from GoogleShetrob import download_file
from progress.bar import IncrementalBar
from pprint import pprint
# os.chdir(os.path.join("Fakultet","Медицинский факультет","Очная","Специалитет","31.05.01"))
# print(os.getcwd())
# print(os.getcwd())
def made_abrev(strok):
    arr_str = strok.split()
    arr_str = arr_str[:1]+[i[0] for i in arr_str[1:]]
    strok = "".join(arr_str)
    return strok

def tested_val(sheet,i,k,val):
    """Забирает значение смежной клетки"""
    for crange in sheet.merged_cells:
        clo, rlo, chi, rhi = crange.bounds
        top_value = sheet.cell(rlo,clo).value
        if rlo <= i and i <= rhi and clo <= (k) and (k) <= chi:
            val = top_value
            break
    return val
def make_gr_arr(arr):
    """Возвращает список с именами групп если есть копии то они именуется как название_группы*номер_группы"""
    res = []
    for i in range(len(arr)):
        if arr.count(arr[i])>=2:
            res.append(arr[i]+f"*{arr[:i].count(arr[i])+1}")
        else:
            res.append(arr[i])
    return res
# Отсортировать список наооборот самый первый это самое большое число,потом по убывающей искать подходящее направление
def pars_lessons(sheet,k):
    date_pars = {}
    act_dat = None
    for j in range(2, sheet.max_row + 1):
        res = sheet.cell(row=j, column=1).value
        if res == None:
            res = tested_val(sheet, j, 3 + k, res)
        if type(res) == datetime.datetime:
            res = res.strftime("%d.%m.%y")
            if res not in date_pars:
                date_pars[res] = []
                act_dat = res
        if act_dat != None:
            val = sheet.cell(row=j, column=3 + k).value
            if val == None:
                val = tested_val(sheet, j, 3 + k, val)
            if val != None:
                para = sheet.cell(row=j, column=2).value
                if para != None:
                    if type(para) == datetime.datetime:
                        para = para.strftime("%d.%m.%y")
                    if type(val) == datetime.datetime:
                        val = val.strftime("%d.%m.%y")
                    para = para.replace("\n", " ")
                    para = para+": " +val
                    while "  " in para:
                        para = para.replace("  ", " ")
                    date_pars[act_dat].append(para)
    for dat in copy.copy(date_pars):
        if date_pars[dat] == []:
            del date_pars[dat]

    return date_pars

def upload_rasp():
    osn_dir = os.path.abspath(os.getcwd())
    # try:
    with open("mgou.json","r") as S:
        osnova = json.load(S)
    # os.chdir("./Fakultet")
    bar = IncrementalBar('Countdown', max=len(list(osnova.keys())))
    for fak in osnova:
        for form_obych in osnova[fak]:
            for level in osnova[fak][form_obych]:
                names_napr = [i for i in osnova[fak][form_obych][level]]
                names_napr.sort(key=len,reverse=True)
                all_groups = {}
                for temp in names_napr:
                    all_groups[temp] = {"ФТД":{"Занятия": {},
                              "Экзамены":{},
                              "Зачеты":{},
                              "Гос.экз":{}},
                              "Учебные дисциплины": {"Занятия": {},
                                      "Экзамены": {},
                                      "Зачеты": {},
                                      "Гос.экз": {}}
                              }
                # for temp in names_napr:
                #     all_groups["расшифровка"][made_abrev(temp)] = temp
                print(all_groups)
                # print(f"{fak}/{form_obych}/{level}",end="")
                # for prog in osnova[fak][form_obych][level]:
                # print(prog)
                # prog_socr = prog.split()[0]
                # put_dir = os.path.join(osn_dir,"Fakultet",fak,form_obych,level,prog_socr)
                put_dir = os.path.join(osn_dir,"Fakultet",fak,form_obych,level)
                # all_groups = {}
                # groups = {"ФТД":{"Занятия": {},
                #           "Экзамены":{},
                #           "Зачеты":{},
                #           "Гос.экз":{}},
                #           "Учебные дисциплины": {"Занятия": {},
                #                   "Экзамены": {},
                #                   "Зачеты": {},
                #                   "Гос.экз": {}}
                #           }
                files = [i for i in os.listdir(put_dir) if i[-4:]=="xlsx" and i[0]!="~"]
                if files == []:
                    continue
                for i in files:
                    try:
                        wb = load_workbook(f"{put_dir}/{i}")
                    # except zipfile.BadZipfile as e:
                    #     try:
                    #         for url in osnova[fak][form_obych][level][prog]:
                    #             download_file(url.split("/")[5], i[-5])
                    #         wb = load_workbook(f"{put_dir}/{i}")
                    #     except:
                    #         continue
                    except:
                        continue
                    # if len(wb.sheetnames) >1:
                    #     print(wb.sheetnames)
                    sheet = wb[wb.sheetnames[0]]
                    title = sheet.cell(row = 1,column = 1).value
                    ser_row,ser_col = 1,1 #Искомые строки и столбцы от search row and search column
                    while type(title) != str or type(title) == datetime.datetime or "Расписание" not in title:
                        if ser_col>sheet.max_column:
                            ser_row +=1
                            ser_col =1
                        title = sheet.cell(row = ser_row,column = ser_col).value
                        if title == None:
                            title = tested_val(sheet, ser_row, ser_col, title)
                        # if type(title) == str or type(title) != datetime.datetime or "Расписание" in title:
                        #     continue
                        ser_col+=1
                    # if title ==None:
                    #     title = tested_val(sheet,1,3,title)
                    if ser_row ==
                    actual_group = None
                    for name in all_groups:
                        if all(i in title for i in name.split()):
                            actual_group = name
                            break
                    arr_gr = []
                    #  Попробую по другому реализовать организацию групп
                    # for gr in range(3,sheet.max_column+1):
                    #     gr_name = sheet.cell(row = 2,column = gr).value
                    #     if gr_name == None:
                    #         gr_name = tested_val(sheet,2,gr,gr_name)
                    #     if gr_name != None:
                    #         arr_gr.append(gr_name)

                    # all_gr= make_gr_arr(arr_gr)
                    if actual_group != None:
                        if "занятий" in title:
                            if "факультативным" in title:
                                for k in range(len(all_gr)):
                                    all_groups[actual_group]["ФТД"]["Занятия"][all_gr[k]] = pars_lessons(sheet, k)
                            else:
                                for k in range(len(all_gr)):
                                    all_groups[actual_group]["Учебные дисциплины"]["Занятия"][all_gr[k]] = pars_lessons(sheet,k)
                        elif "экзаменационной" in title:
                            if "факультативным" in title:
                                for k in range(len(all_gr)):
                                    all_groups[actual_group]["ФТД"]["Экзамены"][all_gr[k]] = pars_lessons(sheet,k)
                            else:
                                for k in range(len(all_gr)):
                                    all_groups[actual_group]["Учебные дисциплины"]["Экзамены"][all_gr[k]] = pars_lessons(sheet, k)
                        elif"зачетной" in title:
                            if "факультативным" in title:
                                for k in range(len(all_gr)):
                                    all_groups[actual_group]["ФТД"]["Зачеты"][all_gr[k]] = pars_lessons(sheet, k)
                            else:
                                for k in range(len(all_gr)):
                                    all_groups[actual_group]["Учебные дисциплины"]["Зачеты"][all_gr[k]] = pars_lessons(sheet, k)
                        elif"аттестационных испытаний" in title:
                            if "факультативным" in title:
                                for k in range(len(all_gr)):
                                    all_groups[actual_group]["ФТД"]["Гос.экз"][all_gr[k]] = pars_lessons(sheet, k)
                            else:
                                for k in range(len(all_gr)):
                                    all_groups[actual_group]["Учебные дисциплины"]["Гос.экз"][all_gr[k]] = pars_lessons(sheet, k)
                all_groups["расшифровка"] = {}
                count_napr = {}
                for temp in names_napr:
                    abrev = made_abrev(temp)
                    if abrev not in count_napr:
                        count_napr[abrev] = 0
                    elif abrev in count_napr:
                        count_napr[abrev] +=1
                    if abrev in all_groups["расшифровка"]:
                        all_groups["расшифровка"][abrev+str(count_napr[abrev])] = temp
                    else:
                        all_groups["расшифровка"][abrev] = temp
                # print(groups)
                #Создаю json файл с расписанием и выхожу в основную директорию
                with open(f"{put_dir}/group.json","w") as f:
                    json.dump(all_groups,f,indent=2, ensure_ascii=False)
                    # print(f"Создан файл {prog}.json")
                    # os.chdir(fak_dir)
    #     bar.next()
    # bar.finish()
# if __name__ == "__main__":
#     upload_rasp()
# a = os.getcwd()
# # put = os.path.join(a,"Fakultet")
# print(put)
# print(os.listdir(put))
if __name__ == "__main__":
    upload_rasp()
