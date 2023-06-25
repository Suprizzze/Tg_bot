import telebot
import requests
import random
from telebot import types
from config import bot

answer = ["Все хорошо", "да отлично", "Превосходно", "пойдет, у тебя как?", "нормально, спасибо"]
answer1 = ["ничего нового", "все новое", "да ничего, а у тебя что нового ?",
           "много чего, но тебе не скажу", "извини, я без настроения"]
answer2 = ["Вуау, красотка", "ммм как будто дьявол смотрит прямо в душу, ужас!", "на тебя похож!",
           "пощади!!! не хотел я это увидеть", "100 из 10 реально красиво", "приятно что в мире "
                                                                            "есть такие прекрасные люди"]

markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
start = types.KeyboardButton("/help")
joke = types.KeyboardButton("Шутка")
markup.add(joke)
markup.add(start)


@bot.message_handler(commands=["start"])
def start_chat(message):
    mess = f"Привет, <b>{message.from_user.first_name} Джан, /help</b>"
    bot.send_message(message.chat.id, mess, parse_mode="html")


@bot.message_handler(commands=["help"])
def help_(message):
    mess = "все команды - как дела, шутка ,что нового,вопросы?(отвечает гифкой да,нет,может быть), " \
           "можете боту отправить свою фотографию на оценку, напишите ' " \
           "пример - рандом snoop dog и получите гифку с ним"

    bot.send_message(message.chat.id, mess, parse_mode="html")
    bot.send_message(message.chat.id, ":P by GeraSupri", reply_markup=markup)


@bot.message_handler()
def start_answer(message):
    mess_text = message.text.lower()
    if "привет" in mess_text:
        mess = f"Привет, {message.from_user.first_name} джан"
        bot.send_message(message.chat.id, mess, parse_mode="html")


def how_are(message):
    mess_text = message.text.lower()
    if "дела" in mess_text or "как ты" in mess_text:
        mess = f"{random.choice(answer)}, {message.from_user.first_name}"
        bot.send_message(message.chat.id, mess, parse_mode="html")


def what_new(message):
    mess_text = message.text.lower()
    if "что нового" in mess_text:
        mess = f"{random.choice(answer1)}, {message.from_user.first_name}"
        bot.send_message(message.chat.id, mess, parse_mode="html")


def gif(message):
    mess_text = message.text.lower()
    if "?" in mess_text:
        response = requests.get("https://yesno.wtf/api")
        pic = response.json()
        mess = pic["image"]
        bot.send_message(message.chat.id, mess, parse_mode="html")


def joke(message):
    mess_text = message.text.lower()
    if "шутка" in mess_text:
        response = requests.get("http://rzhunemogu.ru/RandJSON.aspx?CType=11")
        p = response.text
        mess = p[12:-2]
        bot.send_message(message.chat.id, mess, parse_mode="html")


def random_gif(message):
    mess_text = message.text.lower()
    if "рандом" in mess_text:
        sr = mess_text.split()[1:]
        try:
            response = requests.get(f"https://api.giphy.com/v1/gifs/translate?api_key="
                                    f"fX696cWgpdnP5QKFwwn0ZlFQeEE3977g&s={sr}")
            v = response.json()
            mess = v["data"]['url']
            bot.send_message(message.chat.id, mess, parse_mode="html")
        except TypeError:
            bot.send_message(message.chat.id, "попробуйте другое слово", parse_mode="html")


@bot.message_handler(content_types=["photo"])
def get_user_photo(message):
    bot.send_message(message.chat.id, f"{random.choice(answer2)}")


bot.polling(none_stop=True)
