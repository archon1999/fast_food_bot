import os
import config

import telebot
from telebot import TeleBot, types

from backend.models import BotUser, Product, Order, BotUser
from backend.templates import Messages, Smiles, Keys

from bot import utils
from bot.call_types import CallTypes


def profile_call_handler(bot: TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    keyboard.add(
        utils.make_inline_button(
            text=Keys.PROFILE_EDITED.get(user.lang),
            CallType=CallTypes.Profile_edited
        ),
        utils.make_inline_button(
            text=Keys.BACK.get(user.lang),
            CallType=CallTypes.Back,
            )
        )
    a = {chat_id: 0}
    for users in BotUser.objects.all():
        if users.referal == user:
            a[chat_id] += 1
            print(a)
    text = Messages.PROFILE_CALL_HANDLER.get(user.lang).format(
        uid=chat_id,
        user=user,
        balans=user.balance,
        referal=a[chat_id]
    )
    bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=call.message.id,
        reply_markup=keyboard
    )

def edit_profile(bot: TeleBot, call):
    print(call.data)
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        utils.make_inline_button(
            text=user.full_name,
            CallType=CallTypes.Full_name
        ),
        utils.make_inline_button(
            text=user.contact,
            CallType=CallTypes.Contact
        )
    )
    text = Messages.PROFILE_EDITED.get(user.lang).format(
        full_name=user.full_name,
        contact=user.contact
    )
    bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=call.message.id,
        reply_markup=keyboard
    )