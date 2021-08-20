import os
import config

import telebot
from telebot import TeleBot, types

from backend.models import BotUser, Product, Order
from backend.templates import Messages, Smiles, Keys

from bot import utils, commands
from bot.call_types import CallTypes


def get_order_info(orders, lang):
    pass


def order_call_handler(bot: TeleBot, call):
    pass