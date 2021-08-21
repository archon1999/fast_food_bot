import os
import config

import telebot
from telebot import types

from backend.models import BotUser, BotUser
from backend.templates import Messages, Keys

from bot import utils
from bot.call_types import CallTypes


def profile_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)

    profile_edit_button = utils.make_inline_button(
        text=Keys.PROFILE_EDIT.get(user.lang),
        CallType=CallTypes.ProfileEdit
    )
    back_button =   utils.make_inline_button(
        text=Keys.BACK.get(user.lang),
        CallType=CallTypes.Back,
    )
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(profile_edit_button, back_button)

    referals_count = BotUser.objects.filter(referal=user).count()
    text = Messages.PROFILE_INFO.get(user.lang).format(
        uid=chat_id,
        user=user,
        balans=user.balance,
        referals=referals_count,
    )
    bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=call.message.id,
        reply_markup=keyboard
    )


def profile_edit_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)

    profile_edit_full_name_button = utils.make_inline_button(
        text=user.full_name,
        CallType=CallTypes.ProfileEditFullName,
    )
    profile_edit_contact_button = utils.make_inline_button(
        text=user.contact,
        CallType=CallTypes.ProfileEditContact,
    )
    back_button =   utils.make_inline_button(
        text=Keys.BACK.get(user.lang),
        CallType=CallTypes.Back,
    )
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(profile_edit_full_name_button)
    keyboard.add(profile_edit_contact_button)
    keyboard.add(back_button)
    text = Messages.PROFILE_EDIT.get(user.lang).format(
        full_name=user.full_name,
        contact=user.contact,
    )
    bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=call.message.id,
        reply_markup=keyboard
    )

def profile_edit_full_name_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    if user.bot_state == None:            
        text = Messages.PROFILE_EDIT_FULLNAME.get(user.lang)
        print(user.bot_state)
        bot.send_message(
            chat_id=chat_id,
            text=text,
        )
        user.bot_state = 'edit_name'
        user.save()
        profile_edit_full_name_call_handler(bot, call)
    else:
        profile_edit_full_name(bot, call.message, user)

    

def profile_edit_full_name(bot: telebot.TeleBot, message, user):
    chat_id = message.chat.id
    lang = user.lang
    
    text = Messages.SUCCES_FULL_NAME.get(lang)
    user.full_name = message.text
    user.bot_state = None
    user.save()
    bot.send_message(
        chat_id=chat_id,
        text=text
    )
    profile_call_handler

