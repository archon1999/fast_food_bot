from time import time
import config

from datetime import date, datetime

import telebot
from telebot import types

from bot import utils, admin
from bot.call_types import CallTypes
from bot.states import States

from backend.models import BotUser, ShopCard, Order
from backend.templates import Messages, Keys



def statics_all_member(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.all()
    lang = user.get(chat_id=chat_id).lang
    order = Order.orders.all()

    text = Messages.STATICS_MESSAGE.get(lang).format(
        all_user=user.count(),
        today=user.filter(created__gte=date.today()).count(),
        order=order.count(),
        complated=order.filter(status=Order.Status.COMPLETED).count(),
        conceled=order.filter(status=Order.Status.CANCELED).count(),

    )

    keyboard = admin.admin_keyboard(lang)
    bot.edit_message_text(text=text, chat_id=chat_id,
                            message_id=call.message.id, reply_markup=keyboard)


 
def admin_orders_all(bot: telebot.TeleBot, call):
    order = Order.orders.all()