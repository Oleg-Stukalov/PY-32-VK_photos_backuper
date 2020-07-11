import json
from pprint import pprint
import requests
import freeze

OAUTH_URL = 'https://oauth.vk.com/authorize'
#APP_ID = 7533990  #получен СОИ по ссылке https://vk.com/editapp?act=create
TOKEN_VK = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008' #получен в Нетологии
#TOKEN_YD = '123'
TOKEN_YD = input('Пожалуйста, введите токен учетной записи Яндекс, куда будем сохранять копию фото: ')
print('Сохранен токен Яндекс: ', TOKEN_YD)
#TOKEN_YD = '12345'
###id_korovin = 552934290

class VKUser:
    def __init__(self, id=552934290) -> None:
        self.token_VK = TOKEN_VK
        self.id = id
        self.id2 = id2

    def get_params(self, add_params: dict = None):
        params = {
            'access_token': TOKEN,
            'v': '5.107'
        }
        if add_params:
            # что-то делаем
            # params = расширяем новыми параметрами
            pass
        return params

    def get_request(self, url, params):
        response = requests.get(url, params)
        return response.json()

# Нужно написать программу, которая будет:
#     1. Получать фотографии с профиля. Для этого нужно использовать метод photos.get.
#     2. Сохранять фотографии максимального размера(ширина/высота в пикселях) на Я.Диске.
#     3. Для имени фотографий использовать количество лайков.
#     4. Сохранять информацию по фотографиям в json-файл с результатами.



id_VK = input('Пожалуйста, введите id пользователя Вконтакте, копию фото которого надо сделать (при пустом вводе будет использован id552934290): ')


#pip freeze > requirements.txt #открыть на запись, сохранить вывод freeze???