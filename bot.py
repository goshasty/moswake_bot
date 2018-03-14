import config
import telebot
from telebot import types

from const import *

bot = telebot.TeleBot(config.token_dimas)
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
    bot.send_message(message.chat.id,  BUTTON_POWERED + self.button)
    bot.send_message(message.chat.id,  DAY_CHOSE + self.day)
    bot.send_message(message.chat.id,  TIME_CHOSE + self.time)
    bot.send_message(message.chat.id,  PHONE_CHOSE + self.phone)


def make_keyboard(list,width):
    """
    Show a grid of buttons, which associated with elements of list
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=width,
                                        one_time_keyboard=True)
    keyboard.add(*[types.KeyboardButton(n) for n in list])
    return keyboard

def show_buttons(message):
    keyboard = make_keyboard(categories,1)
    bot.send_message(message.chat.id,INVITE_CATEGORY,reply_markup = keyboard)

def send_photos(message,ID):
    if (ID == 1):
        bot.send_photo(message.chat.id,open('media/wakeboard1.jpg','rb'))
        bot.send_photo(message.chat.id,open('media/wakeboard2.jpg','rb'))
        bot.send_photo(message.chat.id,open('media/wakeboard3.jpg','rb'))
    elif (ID == 2):
        bot.send_photo(message.chat.id,open('media/flyboard1.jpg','rb'))
        bot.send_photo(message.chat.id,open('media/flyboard2.jpg','rb'))
        bot.send_photo(message.chat.id,open('media/flyboard3.jpg','rb'))
    else:
        bot.send_photo(message.chat.id,open('media/winch1.jpg','rb'))
        bot.send_photo(message.chat.id,open('media/winch2.jpg','rb'))
        bot.send_photo(message.chat.id,open('media/winch3.jpg','rb'))

 
def check_categories(text):
    n = 0
    for i in categories:
        if(i == text):
            return n+1
        n = n+1 
    return 0

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
    global p
    n = 0
    for i in text:
        if (((i < '0') or (i > '9')) and (n > 0)):
            return 0
        n = n+1
    if (n == 11 and (text[0] == '7' or text[0] == '8')):
        phone = "+7" + text[1:11]
        p.setPhone(phone)
        return 1
    elif (n == 10):
        phone = "+7" + text
        p.setPhone(phone)
        return 1
    elif((text[0] == '+') and (text[1] == '7') and (n == 12)):
        p.setPhone(text)
        return 1
    else:
        return 0

def check_cancel(text):
    if(text == "/cancel"):
      return 1
    return 0

@bot.message_handler(commands = ['start'])
def start(message):
    """
    Show three buttons
    """ 
    show_buttons(message)

@bot.message_handler(content_types=["text"])
def choose_button(message):
    global p
    global live
    if(check_cancel(message.text) == 1):
         show_buttons(message)
         return
    categoriesID = check_categories(message.text)
    if(categoriesID != 0):
        p = Person(categories[categoriesID-1])
        live = 1
        send_photos(message,categoriesID)
        keyboard = make_keyboard(days,3)
        bot.send_message(message.chat.id,ASK_DAY,reply_markup=keyboard)
        bot.register_next_step_handler(message,ask_day)
    else:
        keyboard = make_keyboard(categories,1)
        bot.send_message(message.chat.id,ASK_CATEGORY_AGAIN,
                         reply_markup=keyboard)
        bot.register_next_step_handler(message,choose_button)


def ask_day(message):
    """
    Check if the day in right format
    if yes - go to time
    """

    global live
    global p
    if(check_cancel(message.text) == 1):
         show_buttons(message)
         return
    if live == 1:
        dayID = check_days(message.text)
        if(dayID != 0):
            p.setDay(message.text)
            keyboard=make_keyboard(times,3)
            bot.send_message(message.chat.id,ASK_TIME,reply_markup=keyboard)
            bot.register_next_step_handler(message,ask_time)
        else:
            keyboard = make_keyboard(days,3)
            bot.send_message(message.chat.id,ASK_DAY_AGAIN,
                             reply_markup=keyboard)
            bot.register_next_step_handler(message,ask_day)
    else:
        bot.send_message(message.chat.id,"lol")

def ask_time(message):
    global live
    global p
    if(check_cancel(message.text) == 1):
         show_buttons(message)
         return
    if live == 1:
        timeID = check_time(message.text)
        if (timeID != 0):
            p.setTime(message.text)
            bot.send_message(message.chat.id,ASK_PHONE)
            bot.register_next_step_handler(message,ask_phone)
        else:
            keyboard = make_keyboard(times,3);
            bot.send_message(message.chat.id,ASK_TIME_AGAIN,
                             reply_markup=keyboard)
            bot.register_next_step_handler(message,ask_time)
    else:
        bot.send_message(message.chat.id,"lol")

def ask_phone(message):
    global live
    global p
    if(check_cancel(message.text) == 1):
         show_buttons(message)
         return
    if live == 1:
        phoneID = check_phone(message.text)
        if (phoneID != 0):
             p.printInformation(message)
             del p
             live = 0
             show_buttons(message)
        else:
            bot.send_message(message.chat.id,ASK_PHONE_AGAIN)
            bot.register_next_step_handler(message,ask_phone)
    else:
        bot.send_message(message.chat.id, "lol")  



if __name__ == '__main__':
     bot.polling(none_stop=True)
