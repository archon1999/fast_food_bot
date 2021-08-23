from bot.states import States
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


def profile_keyboard_hander(user):
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
    return keyboard

def profile_edit_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    keyboard = profile_keyboard_hander(user)
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
    text = Messages.PROFILE_EDIT_FULLNAME.get(user.lang)
    print(user.bot_state)
    bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=call.message.id
    )
    user.bot_state = States.PROFILE_EDIT_FULL_NAME
    user.save()

    

def profile_edit_full_name(bot: telebot.TeleBot, message, user):
    chat_id = message.chat.id
    lang = user.lang
    
    user.full_name = message.text
    user.bot_state = None
    user.save()
    keyboard = profile_keyboard_hander(user)
    text = Messages.SUCCES_FULL_NAME.get(lang).format(full_name=user.full_name,
                                                        contact=user.contact)
    bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=keyboard
    )


def profile_edit_contact(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    user.bot_state = States.PROFILE_EDIT_CONTACT
    user.save()
    text = Messages.CONTACT_NUMBER.get(user.lang)
    bot.edit_message_text(text=text, chat_id=chat_id,
                            message_id=call.message.id)

def profile_edit_contact_number(bot: telebot.TeleBot, message, user):
    chat_id = message.chat.id
    user.contact = message.text
    user.save()
    text = Messages.SUCCES_CONTACT.get(user.lang).format(full_name=user.full_name, contact=user.contact)
    bot.send_message(chat_id=chat_id, text=text,
                        reply_markup=profile_keyboard_hander(user))