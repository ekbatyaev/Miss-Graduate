import telebot
import json
from telebot import types
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
state_storage = StateMemoryStorage()
bot = telebot.TeleBot('Bot_token', state_storage=state_storage)


class MainStates (StatesGroup):
    start_state = State()
    problem_types = State()
    zaglushka = State()
#Keyboard
markup = types.InlineKeyboardMarkup()
item1 = types.InlineKeyboardButton("Погнали", callback_data = 'Начать работу')
markup.add(item1)

markup1 = types.InlineKeyboardMarkup(row_width = 3)
item1 = types.InlineKeyboardButton('1', callback_data='choice_1')
item2 = types.InlineKeyboardButton('2', callback_data='choice_2')
item3 = types.InlineKeyboardButton('3', callback_data= 'choice_3')
item4 = types.InlineKeyboardButton('4', callback_data='choice_4')
item5 = types.InlineKeyboardButton('5', callback_data='choice_5')
item6 = types.InlineKeyboardButton('6', callback_data= 'choice_6')
item7 = types.InlineKeyboardButton('7', callback_data='choice_7')
item8 = types.InlineKeyboardButton('8', callback_data='choice_8')
markup1.add(item1, item2, item3, item4, item5, item6, item7, item8)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot_start_message = bot.send_message(message.from_user.id,f"*Приветственное сообщение*" ,reply_markup=markup, parse_mode = "Markdown")
    put_last_message_id(message.from_user.id, bot_start_message.message_id)
    bot.set_state(message.from_user.id, MainStates.start_state, message.chat.id)

@bot.message_handler(commands=['get_status_info_org_ovs'])
def send_info(message):
    data = load_data("participants.json")
    info = ""
    for i in range(len(data)):
        info += data[i][0] + ": " + str(data[i][1]) + "\n"
    bot_info_message = bot.send_message(message.from_user.id,f"*Статистика на данный момент: *" + "\n\n" + info, parse_mode = "Markdown")
    put_last_message_id(message.from_user.id, bot_info_message.message_id)
    bot.set_state(message.from_user.id, MainStates.start_state, message.chat.id)


@bot.callback_query_handler(state=MainStates.start_state, func = lambda callback: True)
def first_message(message):
    #bot.delete_message(message.from_user.id, messages_id.get(message.from_user.id))
    data = load_data("users.json")
    flag = True
    for i in range(len(data)):
        if (data[i][0] == message.from_user.id) and (data[i][1] != "user"):
            break
        elif (data[i][0] == message.from_user.id) and (data[i][1] == "user"):
            flag = False
            bot.send_message(message.from_user.id, "Ты уже учавствовал в голосовании")
    if (message.data == 'Начать работу') and (flag == True):
        media = [
            telebot.types.InputMediaPhoto(media=open('test.jpg', 'rb')),
            telebot.types.InputMediaPhoto(media=open('test-2.jpg', 'rb')),
            telebot.types.InputMediaPhoto(media=open('test.jpg', 'rb')),
            telebot.types.InputMediaPhoto(media=open('test-2.jpg', 'rb')),
            telebot.types.InputMediaPhoto(media=open('test.jpg', 'rb')),
            telebot.types.InputMediaPhoto(media=open('test-2.jpg', 'rb')),
            telebot.types.InputMediaPhoto(media=open('test.jpg', 'rb')),
            telebot.types.InputMediaPhoto(media=open('test-2.jpg', 'rb'))
            # Добавьте больше изображений по необходимости
        ]
        # bot.send_photo(message.from_user.id, photo=open("test.jpg", "rb"))
        # bot.send_photo(message.from_user.id, photo=open("test-2.jpg", "rb"))
        # bot.send_photo(message.from_user.id, photo=open("test.jpg", "rb"))
        # bot.send_photo(message.from_user.id, photo=open("test-2.jpg", "rb"))
        # bot.send_photo(message.from_user.id, photo=open("test.jpg", "rb"))
        # bot.send_photo(message.from_user.id, photo=open("test-2.jpg", "rb"))
        # bot.send_photo(message.from_user.id, photo=open("test.jpg", "rb"))

        bot.send_media_group(message.from_user.id, media)
        bot_last_mess = bot.send_message(message.from_user.id, f"_Выбери понравившуюся участницу_", reply_markup=markup1, parse_mode = "Markdown")
        put_last_message_id(message.from_user.id, bot_last_mess.message_id)
        bot.set_state(message.from_user.id, MainStates.problem_types)

@bot.callback_query_handler(state=MainStates.problem_types, func = lambda callback: True)
def problem_types(message):
    if message.data == 'choice_1':
        data = load_data("participants.json")
        data[0][1] += 1
        save_data("participants.json", data)
        #bot.delete_message(message.from_user.id, messages_id.get(message.from_user.id))
        bot_problem_types = bot.send_message(message.from_user.id,
                                             f"_Вы проголосовали за первую участницу_",parse_mode="Markdown")
        put_last_message_id(message.from_user.id, bot_problem_types.message_id)
        add_data("users.json", message.from_user.id, "user")
        bot.set_state(message.from_user.id, MainStates.zaglushka)
    elif message.data == 'choice_2':
        data = load_data("participants.json")
        data[1][1] += 1
        save_data("participants.json", data)
        #bot.delete_message(message.from_user.id, messages_id.get(message.from_user.id))
        bot_problem_types = bot.send_message(message.from_user.id,
                                             f"_Вы проголосовали за вторую участницу_", parse_mode="Markdown")
        add_data("users.json", message.from_user.id, "user")
        put_last_message_id(message.from_user.id, bot_problem_types.message_id)
        bot.set_state(message.from_user.id, MainStates.zaglushka)
    elif message.data == "choice_3":
        data = load_data("participants.json")
        data[2][1] += 1
        save_data("participants.json", data)
        #bot.delete_message(message.from_user.id, messages_id.get(message.from_user.id))
        bot_problem_types = bot.send_message(message.from_user.id,
                                             f"_Вы проголосовали за третью участницу_", parse_mode="Markdown")
        add_data("users.json", message.from_user.id, "user")
        put_last_message_id(message.from_user.id, bot_problem_types.message_id)
        bot.set_state(message.from_user.id, MainStates.zaglushka)
    elif message.data == "choice_4":
        data = load_data("participants.json")
        data[3][1] += 1
        save_data("participants.json", data)
        #bot.delete_message(message.from_user.id, messages_id.get(message.from_user.id))
        bot_problem_types = bot.send_message(message.from_user.id,
                                             f"_Вы проголосовали за четвертую участницу_", parse_mode="Markdown")
        add_data("users.json", message.from_user.id, "user")
        put_last_message_id(message.from_user.id, bot_problem_types.message_id)
        bot.set_state(message.from_user.id, MainStates.zaglushka)
    elif message.data == "choice_5":
        data = load_data("participants.json")
        data[4][1] += 1
        save_data("participants.json", data)
        #bot.delete_message(message.from_user.id, messages_id.get(message.from_user.id))
        bot_problem_types = bot.send_message(message.from_user.id,
                                             f"_Вы проголосовали за пятую участницу_", parse_mode="Markdown")
        add_data("users.json", message.from_user.id, "user")
        put_last_message_id(message.from_user.id, bot_problem_types.message_id)
        bot.set_state(message.from_user.id, MainStates.zaglushka)
    elif message.data == "choice_6":
        data = load_data("participants.json")
        data[5][1] += 1
        save_data("participants.json", data)
        #bot.delete_message(message.from_user.id, messages_id.get(message.from_user.id))
        bot_problem_types = bot.send_message(message.from_user.id,
                                             f"_Вы проголосовали за шестую участницу_", parse_mode="Markdown")
        add_data("users.json", message.from_user.id, "user")
        put_last_message_id(message.from_user.id, bot_problem_types.message_id)
        bot.set_state(message.from_user.id, MainStates.zaglushka)
    elif message.data == "choice_7":
        data = load_data("participants.json")
        data[6][1] += 1
        save_data("participants.json", data)
        #bot.delete_message(message.from_user.id, messages_id.get(message.from_user.id))
        bot_problem_types = bot.send_message(message.from_user.id,
                                             f"_Вы проголосовали за седьмую участницу_", parse_mode="Markdown")
        add_data("users.json", message.from_user.id, "user")
        put_last_message_id(message.from_user.id, bot_problem_types.message_id)
        bot.set_state(message.from_user.id, MainStates.zaglushka)
    elif message.data == "choice_8":
        data = load_data("participants.json")
        data[7][1] += 1
        save_data("participants.json", data)
        #bot.delete_message(message.from_user.id, messages_id.get(message.from_user.id))
        bot_problem_types = bot.send_message(message.from_user.id,
                                             f"_Вы проголосовали за восьмую участницу_", parse_mode="Markdown")
        add_data("users.json", message.from_user.id, "user")
        put_last_message_id(message.from_user.id, bot_problem_types.message_id)
        bot.set_state(message.from_user.id, MainStates.zaglushka)
    else:
        bot.set_state(message.from_user.id, MainStates.problem_types)

@bot.message_handler(state=MainStates.zaglushka)
def last_message_final(message):
    bot.send_message(message.from_user.id, f"*Благодарим за отданный голос!*", parse_mode="Markdown")
#Messages id
messages_id = {}
def put_last_message_id(user_id, message_id):
    global messages_id
    messages_id[user_id] = message_id

#Загрузка данных
def load_data(data_file):
    try:
        with open(data_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Если файл не существует, возвращаем пустой список
#Сохранение данных
def save_data(data_file, data):
    with open(data_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

#Добавление данных
def add_data(file_name, col1, col2):
    data = load_data(file_name)
    data.append([col1, col2])
    save_data(file_name, data)
#Удаление данных

def remove_data(file_name, index):
    data = load_data(file_name)
    if 0 <= index < len(data):
        removed = data.pop(index)
        save_data(file_name, data)
        print(f"Удалены данные: {removed}")
    else:
        print("Некорректный индекс!")

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.infinity_polling(skip_pending=True)