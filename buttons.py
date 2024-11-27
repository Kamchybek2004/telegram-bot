from telebot import types


def main_menu_buttons():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('СРС', callback_data="srs")
    btn2 = types.InlineKeyboardButton('Презентация', callback_data="presentation")
    markup.row(btn1, btn2)

    btn3 = types.InlineKeyboardButton('Текст', callback_data="text")
    btn4 = types.InlineKeyboardButton('Расписание', callback_data="schedule")
    markup.row(btn3, btn4)

    return markup