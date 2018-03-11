import config
import telebot
from telebot import types

from const import *

bot = telebot.TeleBot(config.token)
live = 0


class Person:
  def __init__(self,button):
    self.button = button
  def setDay(self,day):
    self.day = day
  def setTime(self,time):
    self.time = time
  def setPhone(self,phone):
    self.phone = phone
  def printInformation(self,message):
    bot.send_message(message.chat.id, "You powered " + self.button)
    bot.send_message(message.chat.id, "Day: " + self.day)
    bot.send_message(message.chat.id, "Time: " + self.time)
    bot.send_message(message.chat.id, "Phone: " + self.phone)


def show_buttons(message):
    keyboard = types.InlineKeyboardMarkup(row_width = 1)
    callback_button_1 = types.InlineKeyboardButton(text = "wakeboard",
                      callback_data = "wakeboard")
    callback_button_2 = types.InlineKeyboardButton(text = "flyboard",
                      callback_data = "flyboard")
    callback_button_3 = types.InlineKeyboardButton(text = "winch",
                      callback_data = "winch")
    keyboard.add(callback_button_1,callback_button_2,callback_button_3)
    bot.send_message(message.chat.id,INVITE_CATEGORY,reply_markup = keyboard)
  

def make_keyboard(list):
    """
    Show a grid of buttons, which associated with elements of list
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3,
                                        one_time_keyboard=True)
    keyboard.add(*[types.KeyboardButton(n) for n in list])
    return keyboard


def check_days(text):
    for i in days:
        if(i == text):
            return 1
    return 0

def check_time(text):
    for i in times:
        if(i == text):
            return 1
    return 0

def check_phone(text):
    n = 0
    for i in text:
        if ((i < '0') or (i > '9')):
            return 0
        n = n+1
    if (n == 10):
        return 1
    else:
        return 0

@bot.message_handler(commands = ['start'])
def start(message):
    """
    Show three buttons
    """ 
    show_buttons(message)



@bot.message_handler(content_types=["text"])
def ask_day(message):
    """
    Check if the day in right format
    if yes - go to time
    """

    global live
    global p
    if live == 1:
        dayID = check_days(message.text)
        if(dayID != 0):
            p.setDay(message.text)
            keyboard=make_keyboard(times)
            bot.send_message(message.chat.id,ASK_TIME,reply_markup=keyboard)
            bot.register_next_step_handler(message,ask_time)
        else:
            bot.send_message(message.chat.id,ASK_DAY_AGAIN)
            bot.register_next_step_handler(message,ask_day)
    else:
        bot.send_message(message.chat.id,"lol")

def ask_time(message):
    global live
    global p
    if live == 1:
        timeID = check_time(message.text)
        if (timeID != 0):
            p.setTime(message.text)
            bot.send_message(message.chat.id,ASK_PHONE)
            bot.register_next_step_handler(message,ask_phone)
        else:
            bot.send_message(message.chat.id,ASK_TIME_AGAIN)
            bot.register_next_step_handler(message,ask_time)
    else:
        bot.send_message(message.chat.id,"lol")

def ask_phone(message):
    global live
    global p
    if live == 1:
        phoneID = check_phone(message.text)
        if (phoneID != 0):
             p.setPhone(message.text)
             p.printInformation(message)
             del p
             live = 0
             show_buttons(message)
        else:
            bot.send_message(message.chat.id,ASK_PHONE_AGAIN)
            bot.register_next_step_handler(message,ask_phone)
    else:
        bot.send_message(message.chat.id, "lol")  


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global p
    global live
    if call.data == "wakeboard":
        p = Person("wakeboard")
    if call.data == "flyboard":
        p = Person("flyboard")
    if call.data == "winch":
        p = Person("winch")
    live = 1
    keyboard = make_keyboard(days)
    bot.send_message(call.message.chat.id,ASK_DAY,reply_markup=keyboard)



if __name__ == '__main__':
     bot.polling(none_stop=True)
