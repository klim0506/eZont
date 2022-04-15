from const import *  # здесь находятся все коды, их не выкладываем на гит хаб, передаем в дискорде
import logging
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
import requests
import sys
import os

start_keyboard = [['/find_dev', '/take_umbrella', '/return_umbrella'], ['/about_us', '/help_me']]
markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=False)


def start(update, context):
    update.message.reply_text(
        "Привет! Через этот бот ты можешь взять зонт в любой точке города!",
        reply_markup=markup
    )


# Взять зонт
def take_umbrella(update, context):
    pass


# Вернуть зонт
def return_umbrella(update, context):
    pass


# Найти ближайший аппарат и вывести фото
def find_dev(update, context):
    # картинка на ЯК с местоположением аппаратов и пользователя
    map_request = "http://static-maps.yandex.ru/1.x/?ll=37.477935,55.663528&spn=0.01,0.01&l=map&pt=37.482074,55.662759,pmdos~37.477911,55.661725,pmdos~37.479909,55.660584,pmdos"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    context.bot.send_photo(chat_id=1740531612, photo=open(map_file, 'rb'))
    # Удаляем за собой файл с изображением.
    os.remove(map_file)


# Вывести фото катры-схемы всех аппаратов
def all_devs(update, context):
    pass


# Написать в поддержку
def answer(update, context):
    pass


# Вывести инструкции по работе программы и бота
def instructions(update, context):
    pass


# instructions functions
# Вывести инструкцию по сдаче зонта
def return_instructions(update, context):
    pass


# Вывести инструкцию по получению зонта
def take_instructions(update, context):
    pass


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("find_dev", find_dev))
    dp.add_handler(CommandHandler("take_umbrella", take_umbrella))
    dp.add_handler(CommandHandler("return_umbrella", return_umbrella))
    dp.add_handler(CommandHandler("all_devs", all_devs))
    dp.add_handler(CommandHandler("answer", answer))
    dp.add_handler(CommandHandler("instructions", instructions))
    dp.add_handler(CommandHandler("return_instructions", return_instructions))
    dp.add_handler(CommandHandler("take_instructions", take_instructions))

    updater.start_polling()

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))


    updater.idle()


if __name__ == '__main__':
    main()



#координаты
#37.477935,55.663528 центр карты
#автоматы
#37.482074,55.662759
#37.477911,55.661725
#37.479909,55.660584