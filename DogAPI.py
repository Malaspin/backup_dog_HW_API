import requests
from tqdm import tqdm
import json
from pprint import pprint


class DogAPI:  #Объявляем класс для хранения методов взаимодействия API Собак и API Диска

    dog_breeds_dict = {}

    def __init__(self):
        self.dog_breeds = ''
        self.api_key = ''
        self.info_images = []

    def get_dog_breeds(self):  #Функция запрашивает у сервера список всех пород и подпород
        url = 'https://dog.ceo/api/breeds/list/all'
        response_get_list = requests.get(url)
        try:
            response_get_list.raise_for_status()
            response_data = response_get_list.json()
            for dog_breeds in tqdm(response_data['message'], desc='Получаю данные о породах ', colour='green'):
                try:
                    self.dog_breeds_dict[dog_breeds] = response_data['message'][dog_breeds]
                except KeyError:
                    self.dog_breeds_dict[dog_breeds].append(response_data['message'][dog_breeds])
        except requests.exceptions.HTTPError as http_err:
            print(f'Ошибка HTTP запроса: {http_err}')
        except Exception as err:
            print(f'Другая ошибка: {err}')

    def dog_image_url_create(self):  #Функция генерирует URL для дальнейшего запроса к API
        try:
            self.dog_breeds_dict[self.dog_breeds]
            if not self.dog_breeds_dict[self.dog_breeds]:
                url = f'https://dog.ceo/api/breed/{self.dog_breeds}/images/random'
                return url
            else:
                sub_breed_list = []
                for sub_breed in tqdm(self.dog_breeds_dict[self.dog_breeds], desc='Генерирую URL', colour='green'):
                    url = f'https://dog.ceo/api/breed/{self.dog_breeds}/{sub_breed}/images/random'
                    sub_breed_list.append(url)
                return sub_breed_list
        except KeyError:
            print('Нет такой породы в списке')

    def get_url_image_dog(self, content):
        dog_get_image_url = []
        if isinstance(content, list):
            for get_url in tqdm(content, desc='Запрашиваю ссылки на изображения ', colour='green'):
                try:
                    response = requests.get(get_url).json()['message']
                    dog_get_image_url.append(response)
                except requests.exceptions.HTTPError as http_err:
                    print(f'Ошибка HTTP запроса: {http_err}')
                except Exception as err:
                    print(f'Другая ошибка: {err}')
            return dog_get_image_url
        else:
            try:
                response = requests.get(content).json()['message']
                return response
            except requests.exceptions.HTTPError as http_err:
                print(f'Ошибка HTTP запроса: {http_err}')
            except Exception as err:
                print(f'Другая ошибка: {err}')

    def write_info_image(self, content):  #Метод пишущий Json лог загруженных картинок
        if isinstance(content, list):
            for image_url in tqdm(content, desc='Сохраняю данные в Json ', colour='green'):
                split_url = image_url.split('/')
                try:
                    response_get_image = requests.get(image_url).content
                    try:
                        with open('load_image.json', 'r', encoding='utf-8') as file:
                            self.info_images = json.load(file)
                    except FileNotFoundError:
                        pass
                    if not any(info_image.get('name') == split_url[-1] for info_image in self.info_images):
                        self.info_images.append({
                            'name': split_url[-1],
                            'sub_breed': split_url[-2],
                            'breed': split_url[-3],
                            'size': f'{len(response_get_image) / 1024}'
                        })
                    with open(r'load_image.json', 'w', encoding='utf-8') as file:
                        json.dump(self.info_images, file, ensure_ascii=False)
                except requests.exceptions.HTTPError as http_err:
                    print(f'Ошибка HTTP запроса: {http_err}')
                except Exception as err:
                    print(f'Другая ошибка: {err}')
        else:
            split_url = content.split('/')
            try:
                response_get_image = requests.get(content).content
                try:
                    with open('load_image.json', 'r', encoding='utf-8') as file:
                        self.info_images = json.load(file)
                except FileNotFoundError:
                    pass
                if not any(info_image.get('name') == split_url[-1] for info_image in self.info_images):
                    self.info_images.append({
                        'name': split_url[-1],
                        'sub_breed': '',
                        'breed': split_url[-2],
                        'size': f'{len(response_get_image) / 1024}'
                    })
                with open(r'load_image.json', 'w', encoding='utf-8') as file:
                    json.dump(self.info_images, file, ensure_ascii=False)
            except requests.exceptions.HTTPError as http_err:
                print(f'Ошибка HTTP запроса: {http_err}')
            except Exception as err:
                print(f'Другая ошибка: {err}')

    def breeds_user_choice(self):  #сервисный метод, вызывается для запроса породы у пользователя
        pprint(f'Доступные породы: {', '.join(self.dog_breeds_dict)}')
        text = input('Выберите породу: ')
        if text in self.dog_breeds_dict:
            self.dog_breeds = text