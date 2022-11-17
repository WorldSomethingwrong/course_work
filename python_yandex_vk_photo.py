import requests
from pprint import pprint
import json
import time
from tqdm import tqdm
import os

vk_token = 'vk1.a.4mxrzevX7uTfrCgODJM17flCWHGHl6POeV-g4fDktlfLEdI72MHgCQVn47hUZ_FSjNN82BInQWnKloazWiM3FgWqiK7YTgcZVCWS_owIeQv60m4ZoPl84_-mkaLwvtncuFthMQih7U-ClK_bo9E5f_yZ40_LSqmADI5KWzDufGIqIrKnPTKY9QvYgjhU4Zs18TwSNcl7p38XflvEdI5zzg'
VK_URL = 'https://api.vk.com/method/photos.get'
YANDEX_URL = 'https://cloud-api.yandex.net:443'
vk_id = input('Введите id пользователя VK: ')
yandex_token = input('Введите токен с полигона YandexDisk: ')
print('Скачивание и загрузка файлов на Яндекс Диск началась.')

def photo_vk():
    params = {
        'owner_id': vk_id,
        'access_token': vk_token,
        'v': '5.131',
        'album_id': 'profile',
        'photo_sizes': '1',
        'extended': '1'
    }
    res = requests.get(VK_URL, params=params)
    json_file = res.json()
    photo_url = json_file['response']['items']
    count = 0
    count_list = []
    info_json = []
    for i in photo_url:
        count += 1
        likes = i['likes']['count']
        sizes = i['sizes'][6]['url']
        size_file = i['sizes'][6]['type']
        filename = f'{likes}.jpg'
        response = requests.get(sizes)
        with open(filename, 'wb') as imgfile:
            imgfile.write(response.content)
        rep_url_yandex = f'{YANDEX_URL}/v1/disk/resources/upload/'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(yandex_token)
        }
        params = {"path": f'/{likes}.jpg', "overwrite": "true"}
        response = requests.get(rep_url_yandex, headers=headers, params=params)
        upload_link = response.json().get('href')
        response = requests.put(upload_link, data=open(f'{likes}.jpg', 'rb'), headers=headers)
        response.raise_for_status()
        dict_json = {f'{likes}': f'{filename}', 'size': f'{size_file}'}
        list_json = [dict_json]
        info_json.append(list_json)
        count_list.append(count)
        for ii in tqdm(count_list):
            time.sleep(1)
    jsonStr = json.dumps(info_json)
    print(jsonStr)
    return


photo_vk()
print('Скачивание и загрузка файлов на Яндекс Диск завершено.')
