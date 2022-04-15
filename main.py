# Главный файл программы, использующий вс остальные функции

# Импортируем необходимые классы.
import logging
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler

#
# # Напишем соответствующие функции.
# # Их сигнатура и поведение аналогичны обработчикам текстовых сообщений.
# def start(update, context):
#     update.message.reply_text(
#         "Привет! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!")
#
#
# def help(update, context):
#     update.message.reply_text(
#         "Я пока не умею помогать... Я только ваше эхо.")
#
#
#
# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5375706253:AAH5KQ50nibA5XpY-MoA61W0udh9YwjLLQ4'
#
#
# # Определяем функцию-обработчик сообщений.
# # У неё два параметра, сам бот и класс updater, принявший сообщение.
# def echo(update, context):
#     # У объекта класса Updater есть поле message,
#     # являющееся объектом сообщения.
#     # У message есть поле text, содержащее текст полученного сообщения,
#     # а также метод reply_text(str),
#     # отсылающий ответ пользователю, от которого получено сообщение.
#     update.message.reply_text(update.message.text)
#
#
# def main():
#     # Создаём объект updater.
#     # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
#     updater = Updater(TOKEN)
#
#     # Получаем из него диспетчер сообщений.
#     dp = updater.dispatcher
#
#     dp.add_handler(CommandHandler("start", start))
#     dp.add_handler(CommandHandler("help", help))
#
#     # Создаём обработчик сообщений типа Filters.text
#     # из описанной выше функции echo()
#     # После регистрации обработчика в диспетчере
#     # эта функция будет вызываться при получении сообщения
#     # с типом "текст", т. е. текстовых сообщений.
#     text_handler = MessageHandler(Filters.text & ~Filters.command, echo)
#
#     # Регистрируем обработчик в диспетчере.
#     dp.add_handler(text_handler)
#     # Запускаем цикл приема и обработки сообщений.
#     updater.start_polling()
#
#     # Ждём завершения приложения.
#     # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
#     updater.idle()

from telegram import ReplyKeyboardMarkup

reply_keyboard = [['/address', '/phone'],
                  ['/site', '/work_time']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def start(update, context):
    update.message.reply_text(
        "Я бот-справочник. Какая информация вам нужна?",
        reply_markup=markup
    )

# Напишем соответствующие функции.
def help(update, context):
    update.message.reply_text(
        "Я бот справочник.")


def address(update, context):
    update.message.reply_text(
        "Адрес: г. Москва, ул. Льва Толстого, 16")


def phone(update, context):
    update.message.reply_text("Телефон: +7(495)776-3030")


def site(update, context):
    update.message.reply_text(
        "Сайт: http://www.yandex.ru/company")


def work_time(update, context):
    update.message.reply_text(
        "Время работы: круглосуточно.")


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("address", address))
    dp.add_handler(CommandHandler("phone", phone))
    dp.add_handler(CommandHandler("site", site))
    dp.add_handler(CommandHandler("work_time", work_time))
    dp.add_handler(CommandHandler("help", help))
    updater.start_polling()

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
