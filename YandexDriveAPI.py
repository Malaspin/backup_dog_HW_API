import requests
from tqdm import tqdm

class YandexDriveAPI:
    base_url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self):
        self.base_headers = {
            'Authorization': ''
        }

    def ensure_api_key(self):
        if not self.base_headers['Authorization']:
            token = input('Введите API Key: ')
            self.base_headers['Authorization'] = f'OAuth {token}'

    def mkdir_ya_drive(self, patch):
        self.ensure_api_key()
        params_mkdir = {
            'path': patch
        }
        response_mkdir = requests.put(self.base_url, headers=self.base_headers, params=params_mkdir)
        try:
            response_mkdir.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            if response_mkdir.status_code == 409:
                pass
            else:
                print(f'Ошибка HTTP запроса: {http_err}')
        except Exception as err:
            print(f'Другая ошибка: {err}')

    def download_image_ya_drive(self, content, patch):  #Метод закидывающий картинку на Диск
        self.ensure_api_key()
        if isinstance(content, list):
            for get_image in tqdm(content, desc='Загружаем данные на Диск ', colour='green'):
                url_split = get_image.split('/')
                param_ya = {
                    'path': f'{patch}/{url_split[-2]}_{url_split[-1]}',
                    'url': get_image
                }
                response_download_image = requests.post(
                    f'{self.base_url}/upload', headers=self.base_headers, params=param_ya
                )
                try:
                    response_download_image.raise_for_status()
                except requests.exceptions.HTTPError as http_err:
                    print(f'Ошибка HTTP запроса: {http_err}')
                except Exception as err:
                    print(f'Другая ошибка: {err}')
        else:
            url_split = content.split('/')
            param_ya = {
                'path': f'{patch}/{url_split[-2]}_{url_split[-1]}',
                'url': content
            }
            response_download_image = requests.post(
                f'{self.base_url}/upload', headers=self.base_headers, params=param_ya
                )
            try:
                response_download_image.raise_for_status()
            except requests.exceptions.HTTPError as http_err:
                print(f'Ошибка HTTP запроса: {http_err}')
            except Exception as err:
                print(f'Другая ошибка: {err}')