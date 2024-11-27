import os
from datetime import datetime
from config import SRS_FOLDER
from config import PRESENTATION_FOLDER



def save_srs_to_txt(user_id, user_name, topic, description):
    ''' Сохранение темы СРС '''
    create_folder_if_not_exists(SRS_FOLDER)

    # Текущая время
    current_date = datetime.now().strftime('%d-%m-%Y')
    current_time = datetime.now().strftime('%H-%M-%S')

    file_name = f"{user_name}_{user_id}_word.txt"
    file_path = os.path.join(SRS_FOLDER, file_name)

    with open(file_path, 'a') as file:
        file.write(f"| Дата: {current_date} Время: {current_time}\n")
        file.write(f"| Тема: {topic}\n")
        file.write(f"| Описание: {description}\n")
        file.write(f"| Пользователь: {user_name}\n")
        file.write(f"| ID: {user_id}\n")
        file.write(f"|-------------------------|\n")

    return file_path

def create_folder_if_not_exists(folder):
    """Создает папку, если она не существует"""
    if not os.path.exists(folder):
        os.makedirs(folder)
    else:
        print(f"Папка существует: {folder}")


# Функция для сохранения данных о презентации в текстовый файл
def save_presentation_to_txt(user_name, user_id, title, description):
    create_folder_if_not_exists(PRESENTATION_FOLDER)

    current_date = datetime.now().strftime('%d-%m-%Y')
    current_time = datetime.now().strftime('%S-%M-%H')

    file_name = f"{user_name}_{user_id}_presentation.txt"
    file_path = os.path.join(PRESENTATION_FOLDER, file_name)

    with open(file_path, 'a') as file:
        file.write(f" Дата: {current_date}  Время: {current_time}\n")
        file.write(f" Тема: {title}\n")
        file.write(f" Описание: {description}\n")
        file.write(f" Пользователь: {user_name}\n")
        file.write(f" ID: {user_id}\n")
        file.write("|--------------------|\n")

    print(f"Данные успешно сохранены в {file_path}")  # Информируем об успешном сохранении
    return file_path  # Возвращаем путь к файлу, если нужно