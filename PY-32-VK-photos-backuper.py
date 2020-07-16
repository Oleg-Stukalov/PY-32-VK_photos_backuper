import json
from pprint import pprint
import requests
import freeze
import os
from os.path import getsize, join
import pathlib

OAUTH_VK_URL = 'https://oauth.vk.com/authorize'
#APP_ID = 7533990  #получен СОИ по ссылке https://vk.com/editapp?act=create
TOKEN_VK = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008' #получен в Нетологии
######!!!!!!!!!!!!!!!!!!!!!!!
TOKEN_YD = 'dsfds'
#TOKEN_YD = input('Пожалуйста, введите токен учетной записи Яндекс, куда будем сохранять копию фото: ')
print('Сохранен токен Яндекс: ', TOKEN_YD)

id_VK = 552934290 #id_korovin
#id_VK = input('Пожалуйста, введите id пользователя Вконтакте, копию фото которого надо сделать (при пустом вводе будет использован id552934290): ')


class VKUser:
    def __init__(self, token: str, user_id: int):
        self.token_VK = token
        self.user_id = user_id

    def get_params(self, add_params: dict = None):
        params = {
            'access_token': self.token_VK,
            'v': '5.77'
        }
        if add_params:
            params.update(add_params)
        #print('*****', params)
        return params

    def get_request(self, url, params):
        response = requests.get(url, params)
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
        #print('===', photo_down_params)
        response = self.get_request('https://api.vk.com/method/photos.get', photo_down_params)
        print(type(response), response)
        max_height = []
        max_width = []
        max_url = []
        photo_url_set = set()
        #сохранение ссылок на фото
        for max_size in json.loads(response.text)['response']['items'][0]['sizes']:
            #print('===', max_size)
            max_height.append(max_size['height'])
            max_width.append(max_size['width'])
            max_url.append(max_size['url'])

            #print('***', max_height, max_width, max_url)
            photo_url_set.add(max_url[max_width.index(max(max_width))])
        likes_list = []
        dates_list = []
        # имя файла по лайкам
        for likes in json.loads(response.text)['response']['items']:
            likes_list.append(likes['likes']['count'])
            dates_list.append(likes['date'])
        for index in range(1, len(likes_list)):
            if likes_list[index] == likes_list[index - 1]:
                likes_list[index] = f'{likes_list[index]}-{dates_list[index]}'
        #print(likes_list, dates_list)
        print(f'Будем сохранять {len(photo_url_set)} следующих фото: {photo_url_set}')



        for number, photo in enumerate(photo_url_set):
            json_output = {}
            response_img = requests.get(photo)
            #print('***', response_img, response_img.text)
            with open(f'{likes_list[number]}.jpg', 'wb') as f:
                #print('===', number, photo)
                f.write(response_img.content)
                ###########
                # создание JSON-отчета
                temp_dic = {'file_name': likes_list[number], 'size': getsize(join(os.walk('.'), likes_list[number]))}
                print(temp_dic)
                json_output.update(temp_dic)
            print(f'Успешно скачан файл {likes_list[number]} по ссылке: {photo}')
            pathlib.Path('.').write_text(json_output, encoding="utf-8")

        return response.json()

#pip freeze > requirements.txt #открыть на запись, сохранить вывод freeze???

user0 = VKUser(TOKEN_VK, id_VK)
#user0.__init__(id_VK)
user0.get_photos()


# Нужно написать программу, которая будет:
#     1. Получать фотографии с профиля. Для этого нужно использовать метод photos.get. add: owner_id; album_id: profile; extended:	1;
#     2. Сохранять фотографии максимального размера(ширина/высота в пикселях) на Я.Диске.
#     3. Для имени фотографий использовать количество лайков.
#     4. Сохранять информацию по фотографиям в json-файл с результатами.