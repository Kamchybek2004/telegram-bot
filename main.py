import telebot
import time
import sys
import signal
from handlers import bot, register_handlers

# Регистрируем обработчики
register_handlers()

def shutdown_bot(signal, frame):
    print(" Остановка работы бота")
    bot.stop_polling()
    sys.exit(0)

# Обработчик Ctrl + C
signal.signal(signal.SIGINT, shutdown_bot)

# Запуск бота
def start_bot():
    while True:
        try:
            bot.polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            time.sleep(15)  # Подождем 15 секунд перед повторной попыткой

if __name__ == '__main__':
    start_bot()
    print('Запуск бота')