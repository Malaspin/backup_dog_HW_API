from time import sleep
from tqdm import tqdm
from DogAPI import DogAPI
from YandexDriveAPI import YandexDriveAPI


if __name__ == '__main__':

    image = DogAPI()
    ya_drive = YandexDriveAPI()
    image.get_dog_breeds()


    should_exit = ''
    while not should_exit:
        sleep(0.1)
        image.breeds_user_choice()
        if not image.dog_breeds:
            print('Введена пустая строка')
            continue
        elif image.dog_breeds not in image.dog_breeds_dict:
            print('Такой породы нет')
            continue
        ya_drive.mkdir_ya_drive(image.dog_breeds)

        with tqdm(total=4, desc='Процесс', colour='green') as pbar:
            dog_url = image.dog_image_url_create()
            pbar.update(1)
            if dog_url:
                    content = image.get_url_image_dog(dog_url)
                    pbar.update(1)
                    image.write_info_image(content)
                    pbar.update(1)
                    ya_drive.download_image_ya_drive(content, image.dog_breeds)
                    pbar.update(1)
            else:
                print('Ошибка получения файла')
        sleep(0.1)
        image.dog_breeds = ''
        should_exit = input('Для продолжения нажмите enter, введите что угодно, что бы закончить ').lower().strip()
        sleep(0.1)