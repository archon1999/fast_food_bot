import os
import config

import telebot
from telebot import types

from backend.models import BotUser, BotUser
from backend.templates import Messages, Smiles, Keys

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
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(profile_edit_full_name_button)
    keyboard.add(profile_edit_contact_button)

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
