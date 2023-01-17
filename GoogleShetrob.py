# # -*- coding: cp1251 -*-
from __future__ import print_function
import io
import pprint

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import json
import os
from progress.bar import IncrementalBar

creds, _ = google.auth.load_credentials_from_file("credentials.json")
def download_file(real_file_id,name_fil):
    """Downloads a file
    Args:
        real_file_id: ID of the file to download
    Returns : IO object with location.

    Load pre-authorized user credentials from the environment.
    for guides on implementing OAuth2 for the application.
    """
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        file_id = real_file_id

        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_id)
        filename = f'./{name_fil}.xlsx'
        fh = io.FileIO(filename, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            # print(F'Download {int(status.progress() * 100)}.'+" -"+name_fil)

    except HttpError as error:
        print(f'Выпало исключение для файла{name_fil}.xlsx')
        try:
            # create drive api client
            service = build('drive', 'v3', credentials=creds)

            file_id = real_file_id

            # pylint: disable=maybe-no-member
            request = service.files().export_media(fileId=file_id,
                                                   mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            filename = f'./{name_fil}.xlsx'
            file = io.FileIO(filename, 'wb')
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                # print(F'Download {int(status.progress() * 100)}. Вторая попытка успешна')

        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None

        return None

    return None#file.getvalue()
def fak_domload():
    # try:
    # print("Directory",os.getcwd())
    zapret = ("|","<",">","*","/","\\","?",":",";")
    # osn_dir = os.getcwd()
    with open("mgou.json","r") as f:
        mgo = json.load(f)
        bar = IncrementalBar('Countdown', max=len(list(mgo.keys())))
        # pprint.pprint(mgo)
        os.chdir("Fakultet")
        print(os.getcwd())
        for i in mgo: # Факультеты
            if not os.path.isdir(i):
                os.mkdir(i)
            os.chdir(i)
            for j in mgo[i]: #форма обучения
                if not os.path.isdir(j):
                    os.mkdir(j)
                os.chdir(j)
                for k in mgo[i][j]:# Уровень
                    if not os.path.isdir(k):
                        os.mkdir(k)
                    os.chdir(k)
                    cnt = 0
                    for t in mgo[i][j][k]:#Программы обучения
                        # if not os.path.isdir(t.split()[0]):
                        #     os.mkdir(t.split()[0])
                        # os.chdir(t.split()[0])
                        for url in mgo[i][j][k][t]:
                            cnt+=1
                            if any(i for i in zapret if i in t):
                                for non_zn in zapret:
                                    t = t.replace(non_zn," ")#Удаляет запрещенный фаловой системой знаки
                            file_id = url.split("/")[5]
                            download_file(file_id,f"{t.split()[0]} {cnt}")
                            # print(f"{t} {cnt} создался")

                    os.chdir("..")
                os.chdir("..")
            os.chdir("..")
        os.chdir("..")
        # bar.next()
    # bar.finish()
    # return True
def update():
    print("Начало обновление базы расписания")
    fak_domload()
    print("Расписание обновлено")
if __name__ == "__main__":
    update()