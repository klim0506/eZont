from const import *
from files.API_maps import *
from files.user_actions import *
from telegram.ext import Updater, CommandHandler
from telegram import ReplyKeyboardMarkup, InputMessageContent


start_keyboard = [['/find_dev', '/take_umbrella', '/return_umbrella'], ['/all_devs', '/help_me']]
start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=False)


def start(update, context):
    update.message.reply_text(
        "Привет! Через этот бот ты можешь взять зонт в любой точке города!",
        reply_markup=start_markup
    )


# Взять зонт
def take_umbrella(update, context):
    nums_keyboard = [['/1111', '/2222', '/3333']]
    nums_markup = ReplyKeyboardMarkup(nums_keyboard, one_time_keyboard=True, input_field_placeholder='device_id?')

    update.message.reply_text(
        "Введите номер аппарата",
        reply_markup=nums_markup
    )

    # ToDo: принять номер аппарата, для примера взят 1111
    device_system_index = 1111

    if not returned_umbrella('db/data.db', device_system_index):
        update.message.reply_text("Нельзя взять больше 3 зонтов на одного пользователя!", reply_markup=start_markup)

    else:
        update.message.reply_text("""Возьмите зонт☂ 
Сдать его можно в любом аппарате eZont""", reply_markup=start_markup)


# Вернуть зонт
def return_umbrella(update, context):
    nums_keyboard = [['/1111', '/2222', '/3333']]
    nums_markup = ReplyKeyboardMarkup(nums_keyboard, one_time_keyboard=True)

    update.message.reply_text(
        "Введите номер аппарата",
        reply_markup=nums_markup
    )

    # ToDo: принять номер аппарата, для примера взят 1111
    device_system_index = 1111

    if not taken_umbrella('db/data.db', device_system_index):
        update.message.reply_text("Пока что у вас нет зонтов, чтобы их вернуть", reply_markup=start_markup)

    else:
        update.message.reply_text("""Спасибо☂ 
Вы всегда можете взять зонт в любом аппарате eZont""", reply_markup=start_markup)


# Найти ближайший аппарат и вывести фото
def find_dev(update, context):
    # ToDo: принять координаты у пользователя, пока что их заменяет переменная user_coordinates,
    #  которая указывает на наш технопарк
    user_coordinates = (55.660968, 37.476088)

    data = near_app('db/data.db', 55.660968, 37.476088)
    near_app_map(user_coordinates, (data['latitude'], data['longitude']))

    user_id = update.message['chat']['id']
    # отправляем фотографию карты с отметками
    context.bot.send_photo(chat_id=user_id, photo=open('files/images/near_app_map.jpg', 'rb'))
    # отправляем данные об аппарате
    update.message.reply_text(f"""Мы нашли ближайший аппарат!
    
🌍   Расположение - {data['place']}
☂   Зонтов - {data['fill_cell']}
🔍   Свободных ячеек - {data['free_cell']}""")


# Вывести фото катры-схемы всех аппаратов
def all_devs(update, context):
    all_app_map('db/data.db')  # Обновляем карту по БД
    user_id = update.message['chat']['id']
    # отправляем фотографию карты с отметками
    context.bot.send_photo(chat_id=user_id, photo=open('files/images/all_app_map.jpg', 'rb'))


# Написать в поддержку
def support(update, context):
    update.message.reply_text("Не нашли ответ на свой вопрос? Просто напишите его следующим сообщением")
    # ToDo: прочитать ответ на сообщение и занести его в БД


# Вывести инструкции по работе программы и бота
def send_instructions(update, context):
    instr_keyboard = [['/how_to_return_umbrella', '/how_to_take_umbrella'], ['/description_of_project', '/support']]
    markup = ReplyKeyboardMarkup(instr_keyboard, one_time_keyboard=True)
    update.message.reply_text("Здесь приведены ответы на частые вопросы. Чем помочь?", reply_markup=markup)


def return_instructions(update, context):
    update.message.reply_text(instruction('files/txt/how_to_return_umbrella.txt'), reply_markup=start_markup)


def take_instructions(update, context):
    update.message.reply_text(instruction('files/txt/how_to_take_umbrella.txt'), reply_markup=start_markup)


def description(update, context):
    update.message.reply_text(instruction('files/txt/description.txt'), reply_markup=start_markup)


def main():
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("find_dev", find_dev))
    dp.add_handler(CommandHandler("take_umbrella", take_umbrella))
    dp.add_handler(CommandHandler("return_umbrella", return_umbrella))
    dp.add_handler(CommandHandler("all_devs", all_devs))
    dp.add_handler(CommandHandler("support", support))
    dp.add_handler(CommandHandler("help_me", send_instructions))
    dp.add_handler(CommandHandler("how_to_return_umbrella", return_instructions))
    dp.add_handler(CommandHandler("how_to_take_umbrella", take_instructions))
    dp.add_handler(CommandHandler("description_of_project", description))

    updater.start_polling()

    dp.add_handler(CommandHandler("start", start))

    updater.idle()


if __name__ == '__main__':
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    main()
