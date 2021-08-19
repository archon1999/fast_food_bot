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
    text = Messages.PROFILE_CALL_HANDLER.get(user.lang)
    bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=call.message.id,
        # reply_markup=
    )