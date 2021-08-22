import os

from telebot import util

import config

import telebot
from telebot import types

from backend.models import BotUser, Info, Review
from backend.templates import Messages, Keys

from bot import utils
from bot.call_types import CallTypes

def get_info_image_path(info: Info):
    return os.path.join(config.APP_DIR, info.image.name)


def get_info_info(info: Info, lang: str):

    return Messages.INFO_MESSAGE.get(lang).format(
        title=info.get_title(lang),
        description=info.get_description(lang),
    )

def get_button(info: Info, lang):
    button = []
    for inf in info.comments.all():
        button.append(
            utils.make_inline_button(
                text=inf.name,
                CallType=CallTypes.Ratings,
                balls=inf.name1
            )
        )
    back_button = utils.make_inline_button(
        text=Keys.BACK.get(lang),
        CallType=CallTypes.Back,
    )
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*button)
    keyboard.add(back_button)
    return keyboard

def yes_or_no(lang):
    yes = utils.make_inline_button(
        text=Keys.YES_KEYBOARD.get(lang),
        CallType=CallTypes.Yes_or_No,
        yes="yes"
    )
    no = utils.make_inline_button(
        text=Keys.NO_KEYBOARD.get(lang),
        CallType=CallTypes.Yes_or_No,
        no = "no"
    )
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(yes, no)
    print(keyboard)
    return keyboard


def info_message_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    info = Info.objects.get(id=1)
    keyboard = get_button(info, user.lang)
    
    image_path = get_info_image_path(info)
    product_info = get_info_info(info, user.lang)
    with open(image_path, 'rb') as photo:
        bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=product_info,
            reply_markup=keyboard
        )

def rating_balls_call_handler(bot: telebot.TeleBot, call):
    call_type = CallTypes.parse_data(call.data)
    balls = call_type.balls
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    review = Review.objects.create(user=user, rating=balls)
    lang = user.lang
    text = Messages.RATING_MESSAGE.get(lang)
    bot.delete_message(chat_id=chat_id, message_id=call.message.id)
    bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=yes_or_no(lang)
    )

def yes_or_no_message_handler(bot: telebot.TeleBot, call):
    print(call.data)