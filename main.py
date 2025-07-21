import requests
import json
from tqdm import tqdm
from pprint import pprint

class DogAPI:  #Объявляем класс для хранения методов взаимодействия API Собак и API Диска

    base_ya_url = 'https://cloud-api.yandex.net/v1/disk/resources'
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

    def  get_url_image_dog(self, content):
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


    def download_image_ya_drive(self, content):  #Метод закидывающий картинку на Диск
        self.ensure_api_key()
        headers_ya = {
            'Authorization': f'OAuth {self.api_key.strip()}'
        }
        if isinstance(content, list):
            for get_image in tqdm(content, desc='Загружаем данные на Диск ', colour='green'):
                url_split = get_image.split('/')
                base_param_ya = {
                    'path': f'{self.dog_breeds}/{url_split[-2]}_{url_split[-1]}',
                    'url': get_image
                }
                response_download_image = requests.post(
                    f'{self.base_ya_url}/upload', headers=headers_ya, params=base_param_ya
                )
                try:
                    response_download_image.raise_for_status()
                except requests.exceptions.HTTPError as http_err:
                    print(f'Ошибка HTTP запроса: {http_err}')
                except Exception as err:
                    print(f'Другая ошибка: {err}')
        else:
            url_split = content.split('/')
            base_param_ya = {
                'path': f'{self.dog_breeds}/{url_split[-2]}_{url_split[-1]}',
                'url': content
            }
            response_download_image = requests.post(
                f'{self.base_ya_url}/upload', headers=headers_ya, params=base_param_ya\
                )
            try:
                response_download_image.raise_for_status()
            except requests.exceptions.HTTPError as http_err:
                print(f'Ошибка HTTP запроса: {http_err}')
            except Exception as err:
                print(f'Другая ошибка: {err}')

    def put_ya_mkdir(self):  #Метод создания папки на Диске
        self.ensure_api_key()
        headers_ya = {
            'Authorization': f'OAuth {self.api_key.strip()}'
        }
        base_param_ya = {
            'path': self.dog_breeds,
        }
        response_mkdir = requests.put(self.base_ya_url, headers=headers_ya, params=base_param_ya)
        try:
            response_mkdir.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            if response_mkdir.status_code == 409:
                pass
            else:
                print(f'Ошибка HTTP запроса: {http_err}')
        except Exception as err:
            print(f'Другая ошибка: {err}')

    def breeds_user_choice(self):  #сервисный метод, вызывается для запроса породы у пользователя
        pprint(f'Доступные породы: {', '.join(self.dog_breeds_dict)}')
        text = input('Выберите породу: ')
        if text in self.dog_breeds_dict:
            self.dog_breeds = text

    def ya_drive_key_add(self):  #Сервисный метод, вызывается для первого запроса ключа
        self.api_key = input('Введите api_key Яндекс Диска: ')

    def ensure_api_key(self):  #блок проверяющий наличие токена, и запрашивающий информацию от пользователя, если ключа нет
        if not self.api_key:
            self.ya_drive_key_add()


if __name__ == '__main__':

    image = DogAPI()
    image.get_dog_breeds()


    should_exit = ''
    while not should_exit:
        image.breeds_user_choice()
        if not image.dog_breeds:
            print('Введена пустая строка')
        elif image.dog_breeds not in image.dog_breeds_dict:
            print('Такой породы нет')
        image.put_ya_mkdir()

        with tqdm(total=4, desc='Процесс', colour='green') as pbar:
            dog_url = image.dog_image_url_create()
            pbar.update(1)
            if dog_url:
                    content = image.get_url_image_dog(dog_url)
                    pbar.update(1)
                    image.write_info_image(content)
                    pbar.update(1)
                    image.download_image_ya_drive(content)
                    pbar.update(1)
            else:
                print('Ошибка получения файла')

        should_exit = input('Для продолжения нажмите enter, введите что угодно, что бы закончить ').lower().strip()