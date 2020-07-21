import json
from pprint import pprint
import pip
import requests
import freeze
import os
from os.path import getsize, join
import pathlib

OAUTH_VK_URL = 'https://oauth.vk.com/authorize'
YD_URL = 'https://cloud-api.yandex.net:443/v1/disk'
YANDEX_UPLOAD_URL = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
#APP_ID = 7533990  #получен СОИ по ссылке https://vk.com/editapp?act=create
TOKEN_VK = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008' #получен в Нетологии
######!!!!!!!!!!!!!!!!!!!!!!!
TOKEN_YD = '423'
#TOKEN_YD = input('Пожалуйста, введите токен учетной записи Яндекс, куда будем сохранять копию фото: ')
YD_OAUTH = {'Authorization': f'OAuth {TOKEN_YD}'}
print('Сохранен токен Яндекс: ', TOKEN_YD)

id_VK = 552934290 #id_korovin
#id_VK = input('Пожалуйста, введите id пользователя Вконтакте, копию фото которого надо сделать (при пустом вводе будет использован id552934290): ')


class VKUser:
    def __init__(self, token: str, user_id: int, params=None, headers=None, files_for_upload=None):
        self.token_VK = token
        self.user_id = user_id
        self.params = params
        self.headers = headers
        self.files_for_upload = files_for_upload


    def get_params(self, add_params: dict = None):
        params = {
            'access_token': self.token_VK,
            'v': '5.77'
        }
        if add_params:
            params.update(add_params)
        #print('*****', params)
        return params

    def get_request(self, url, params, headers=None):
        response = requests.get(url, params=params)
        return response.json()

    def put_request(self, url, params, headers):
        response = requests.put(url, params=params, headers=headers)
        return response.json()

    def get_photos(self):
        #доп параметры для скачивания фото
        photo_down_params = self.get_params(
            add_params = {
                'owner_id': id_VK,
                'album_id': 'profile',
                'extended': 1
            }
        )
        response = self.get_request('https://api.vk.com/method/photos.get', photo_down_params)
        max_height = []
        max_width = []
        max_url = []
        photo_url_set = set()
        #сохранение ссылок на фото
        for max_size in response['response']['items'][0]['sizes']:
            max_height.append(max_size['height'])
            max_width.append(max_size['width'])
            max_url.append(max_size['url'])
            photo_url_set.add(max_url[max_width.index(max(max_width))])
        likes_list = []
        dates_list = []
        # имя файла по лайкам
        for likes in response['response']['items']:
            likes_list.append(likes['likes']['count'])
            dates_list.append(likes['date'])
        for index in range(1, len(likes_list)):
            if likes_list[index] == likes_list[index - 1]:
                likes_list[index] = f'{likes_list[index]}-{dates_list[index]}'
        print(f'Будем сохранять {len(photo_url_set)} следующих фото: {photo_url_set}')

        json_output = []
        files_for_upload = []
        for number, photo in enumerate(photo_url_set):
            response_img = requests.get(photo)
            #print('***', response_img, response_img.text)
            with open(f'{likes_list[number]}.jpg', 'wb') as f:
                f.write(response_img.content)
                # создание JSON-отчета
                temp_dic = {'file_name': likes_list[number], 'size': getsize(f'{likes_list[number]}.jpg')}
                json_output.append(temp_dic)
                files_for_upload.append(f'{likes_list[number]}.jpg')
                #self.files_for_upload.append(f'{likes_list[number]}.jpg')
            print(f'Успешно скачан файл {likes_list[number]} по ссылке: {photo}')
            # сохраняю в json
            with open('output.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(json_output, ensure_ascii=False))
        print('Успешно сохранен лог файл: output.json')
        print('===111', files_for_upload)
        return files_for_upload
        print('===222', self.files_for_upload, files_for_upload)
        print('===333', get_photos())


    def yandex_folder(self):
        yandex_oauth_header = {
            'Accept': 'application/json',
            'Authorization': f'OAuth {TOKEN_YD}'
        }
        yandex_folder_url = f'{YD_URL}{"/resources"}'
        #доп параметры для создания папки ЯД
        yandex_folder_params = {
                'path': f'{"id_VK-"}{id_VK}',
                'overwrite': 'true'
            }
        #print(yandex_folder_params)
        response = self.put_request(yandex_folder_url, params=yandex_folder_params, headers=yandex_oauth_header)
        print('+++', type(response), response)
        self.yandex_upload(self.files_for_upload)
        return response

    def yandex_upload(self, files_for_upload):
        #print('!!!!!!', files_for_upload)
        yandex_oauth_header = {
            'Accept': 'application/json',
            'Authorization': f'OAuth {TOKEN_YD}'
        }
        for file in files_for_upload:
            # доп параметры для получения ссылки на загрузку файла
            yandex_upload_params = {
                'path': file
            }
            response = requests.get(YANDEX_UPLOAD_URL, params=yandex_upload_params, headers=yandex_oauth_header)
            #print('!!!!!!!!!', response, response.text)
            put_url = response.json().get('href')
            #открыть файл на БИНАР чтение, передать его в яндекс!
            with open(file, 'rb') as f:
                data_4upload = f.read()
            print('*****', put_url)
            response_upload = requests.put(put_url, data=data_4upload)
            print('Ответ сервера (загрузка файла): ', response_upload)
            print(response_upload.text)
            print(f'Файл: "{file}" - успешно загружен!')
        return print(f'Все файлы успешно загружены в Яндекс.диск!')

#pip freeze > requirements.txt #открыть на запись, сохранить вывод freeze???

user0 = VKUser(TOKEN_VK, id_VK)
user0.get_photos()
user0.yandex_folder()
