import telebot
from file_utils import save_srs_to_txt
from config import SRS_COMPLETED_FOLDER
from config import PRESENTATION_COMPLETED_FOLDER
from config import PRESENTATION_FOLDER
from buttons import main_menu_buttons

from file_utils import save_presentation_to_txt
from config import TOKEN
from  telebot import types
import os
import logging


bot = telebot.TeleBot(TOKEN)


# Словарь для хранения временных данных пользователей
user_data = {}

def register_handlers():
    """Регистр всех обработчиков"""

    ''' Основное описание '''
    @bot.message_handler(commands=['start'])
    def main(message):
        markup = main_menu_buttons()
        user_name = message.from_user.first_name
        bot.send_message(message.chat.id,
                         f"Салам <b>{user_name}</b>. Этот телеграм-бот поможет вам, если у вас начинаются "
                         "экзамены или приближается время сдачи студенческих работ.\n"
                         "<b>Примечание:</b> Бот не выполняет автоматически такие услуги как 'срс' и 'презентация'.\n"
                         "Телеграмм-бот служить как посредник между заказчиком и человеком который выполняет ваши задания.\n\n"
                         "<b>Бот предоставляет следующие услуги:\n\n</b>"
                         "1. <b>\U0001F4C4Текстовые работы:</b> Сканируйте фото, чтобы получить текст в электронном виде.\nНажмите на кнопку «Текст», чтобы начать.\n"
                         "2. <b>\U0001F4DDСРС:</b> Подготовка СРС. Нажмите на кнопку «СРС», чтобы отправить тему и описание.\n"
                         "3. <b>\U0001F4C8Презентация:</b> Создание презентации. Нажмите на кнопку «Презентация», чтобы отправить запрос.\n"
                         "4. \U0001F4C5График уроков\n\n"
                         "<b>Категории «Текст» и «График уроков» будут доступны в ближайшее время. Ожидайте!</b>"
                         " "
                         "Выберите одну из категорий:",
                         reply_markup=markup, parse_mode='html')

    '''
    @bot.callback_query_handler(func=lambda callback: True)
    def callback_msg(callback):
        user_name = callback.message.from_user.first_name

        if callback.data == 'srs':
            start_srs(callback.message)
        elif callback.data == 'presentation':
            handle_presentation(callback.message)
        elif callback.data == 'text':
            bot.send_message(callback.message.chat.id, f"{user_name} вы выбрали категорию Текст")
        elif callback.data == 'schedule':
            bot.send_message(callback.message.chat.id,
                             f"{user_name} вы выбрали категорию Расписание")
        else:
            bot.send_message(callback.message.chat.id, "Ошибка 100. Неверная команда")

    '''


    ''' Команды и функции '''

    ''' Команда /srs для начала ввода темы и описания СРС '''
    #@bot.message_handler(commands=['srs'])
    @bot.callback_query_handler(func=lambda callback: callback.data == 'srs')
    def start_srs(callback):
        user_id = callback.message.from_user.id
        #user_data[user_id] = {'topic': callback.message.text}
        user_name = callback.from_user.first_name
        bot.send_message(callback.message.chat.id, "Пожалуйста <b>{0}</b>, <b>введите тему для вашей СРС:</b>\n"
                                                   "<b>Обратите внимание:</b> убедитесь, что вводите корректную информацию.".format(user_name), parse_mode='html')
        bot.register_next_step_handler(callback.message, get_srs_topic)


    def get_srs_topic(message):
        user_id = message.from_user.id
        user_data[user_id] = {'topic': message.text}
        bot.reply_to(message, "Пожалуйста, <b>введите описание для вашей СРС:</b>\n"
                              "<b>Обратите внимание:</b> убедитесь, что вводите корректную информацию.", parse_mode='html')
        bot.register_next_step_handler(message, get_srs_description)

    def get_srs_description(message):
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        description = message.text

        # Сохраняем данные пользователя
        user_data[user_id]['description'] = description
        confirm_srs(message, description)


    def confirm_srs(message, description):
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        #Потверждение
        confirm_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        confirm_markup.add('Да','Нет')
        bot.reply_to(message, "<b>Вы уверенны, что хотите отправить данные?</b>\n"
                              f"<b>Тема:</b>{user_data[user_id]['topic']}\n"
                              f"<b>Описание:</b>{user_data[user_id]['description']}", reply_markup=confirm_markup, parse_mode='html')
        bot.register_next_step_handler(message, lambda m: process_confirmation(m, user_id, description))

    def process_confirmation(message, user_id, description):
        user_name = message.from_user.first_name
        file_user = f"{user_name}_{user_id}.txt"

        if message.text.lower() == 'да':
            # Сохраняем данные
            # topic = user_data[user_id]['topic']
            #description = user_data[user_id]['description']
            #save_srs_to_txt(user_id, user_name, topic, description)

            # Сохраняем данные в текстовый файл
            file_path = save_srs_to_txt(user_id, user_name, user_data[user_id]['topic'], description)
            bot.reply_to(message, f"Спасибо <b>{user_name}</b>! Ваш СРС сохранен. <b>Ожидайте.</b>"
                                  f"\n Для того чтобы получить срс или проверить: /send_srs", parse_mode='html')
            print(f'Пользователь {user_name}_{user_id} отправил  вам заказ \n')
            print(f'Файл с заданиями находиться в srs_data/{file_user}')
            #bot.reply_to(message, "Спасибо! Ваш СРС сохранен.")
        elif message.text.lower() == 'нет':
            bot.reply_to(message, "Отмена отправки. Вы можете ввести данные заново.")
            start_srs(message)  # Перезапускаем процесс ввода
        else:
            bot.reply_to(message, "Пожалуйста, выберите ,<b>'Да'</b> или <b>'Нет'</b>.",parse_mode='html')
            confirm_srs(message, description)  # Снова запрашиваем подтверждение




    # Получение id пользователя
    @bot.message_handler(commands=['id'])
    def get_id(message):
        user_name = message.from_user.first_name
        user_id = message.from_user.id
        bot.reply_to(message, f'ID: {user_name}_{user_id}')


    # Команда для отправки готового файла обратно пользователю
    @bot.message_handler(commands=['send_srs'])
    def send_srs_file(message):
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        file_name = f"{user_name}_{user_id}.docx"  # или .docx
        file_path = os.path.join('srs_completed', file_name)

        try:
            # Проверка существования директории
            if os.path.exists(file_path):
                # Получение файла и отправка к пользователю
                with open(file_path, 'rb') as file:
                    bot.send_document(message.chat.id, file)
                    bot.reply_to(message, "Вот ваш готовый СРС!")
                    print(f"Файл отправлен на адрес пользователя {user_name}_{user_id}")
            else:
                bot.reply_to(message,
                             f"Файл {file_name} не найден в папке {SRS_COMPLETED_FOLDER}. Проверьте правильность имени файла и наличие.")
        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка: {e}")


    ''' Презентация '''
    #@bot.message_handler(commands=['presentation'])
    @bot.callback_query_handler(func=lambda callback: callback.data == 'presentation')
    def handle_presentation(callback):
        user_name = callback.from_user.first_name
        bot.send_message(callback.message.chat.id, f'{user_name}, введите тему презентации:')
        bot.register_next_step_handler(callback.message,get_presentation_title)

    def get_presentation_title(message):
        user_id = message.from_user.id
        title = message.text

        msg = bot.reply_to(message, "Введите описание презентации:")
        bot.register_next_step_handler(msg, lambda m:get_description(m, user_id, title))


    def get_description(message, user_id, title):
        try:
            description = message.text
            user_name = message.from_user.first_name

            #Сохраняем данные пользователя
            user_data[user_id] = {'topic':title, 'description': description}

            #save_presentation_to_txt(user_name, user_id, title, description)
            #confirm_presentation(message)
            #bot.reply_to(message, "Данные для презентации успешно сохранены! Ожидайте получение. \n"
            #                      "Для того чтобы получить презентацию или проверить: /send_presentation")

            confirm_presentation(message)
        except Exception as e:
            bot.reply_to(message, "Произошла ошибка при обработке вашего ввода.")


    def confirm_presentation(message):
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        topic = user_data[user_id]['topic']
        description = user_data[user_id]['description']
        confirm_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        confirm_markup.add('Да','Нет')

        bot.reply_to(message,f"Вы уверенны, что хотите отправить следующие данные?\n"
                             f"Тема: {topic}\n"
                             f"Описание: {description}\n"
                             f"Введите 'Да' для подтверждения или 'Нет' для отмены.", reply_markup=confirm_markup)
        bot.register_next_step_handler(message, handle_confirmation)  # Переход к подтверждению

    @bot.message_handler(func=lambda message: message.from_user.id in user_data and message.text.lower() in ['да', 'нет'])
    def handle_confirmation(message):
        user_id = message.from_user.id
        if message.text.lower() == 'да':
            user_name = message.from_user.first_name
            topic = user_data[user_id]['topic']
            description = user_data[user_id]['description']

            # Сохраняем данные в текстовый файл
            save_presentation_to_txt(user_name, user_id, topic, description)

            bot.reply_to(message, "Спасибо! Ваша презентация успешно сохранена.\n"
                                  "Ожидайте получения презентацию.\n"
                                  "Для получения презентацию или проверить: /send_presentation")
        elif message.text.lower() == 'нет':
            bot.reply_to(message, "Отмена отправки. Вы можете ввести данные заново.")
            handle_presentation(message)  # Перезапускаем процесс ввода
        else:
            bot.reply_to(message, "Пожалуйста, выберите 'Да' или 'Нет'.")
            confirm_presentation(message)  # Снова запрашиваем подтверждение


    # Обработчик команды для отправки готовой презентации
    @bot.message_handler(commands=['send_presentation'])
    def send_presentation(message):
        user_name = message.from_user.first_name
        user_id = message.from_user.id
        file_name = f"{user_name}_{user_id}_presentation.pptx"  # Убедитесь, что это имя вашего файла PowerPoint
        file_path = os.path.join('presentation_completed', file_name)

        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                bot.send_document(message.chat.id, file)
                bot.reply_to(message, "Вот ваша готовая презентация!")
        else:
            bot.reply_to(message, "Презентация не найдена. Убедитесь, что она сохранена.")




    # Текст
    @bot.callback_query_handler(func=lambda callback: callback.data == 'text')
    def handle_text(callback):
        user_name = callback.from_user.first_name
        bot.send_message(callback.message.chat.id, f"{user_name}, вы выбрали категорию Текст.")

    # Расписание
    @bot.callback_query_handler(func=lambda callback: callback.data == 'schedule')
    def handle_schedule(callback):
        user_name = callback.from_user.first_name
        bot.send_message(callback.message.chat.id, f"{user_name}, вы выбрали категорию Расписание.")