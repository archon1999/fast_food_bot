import config

import telebot
from telebot import TeleBot, types

from django.core.paginator import Paginator

from backend.models import BotUser, Order
from backend.templates import Messages, Smiles, Keys

from bot import utils
from bot.call_types import CallTypes
from bot.shopcard import get_purchases_info, ordering_start


def orders_call_handler(bot: TeleBot, call):
    call_type = CallTypes.parse_data(call.data)
    page_number = call_type.page

    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang

    orders = user.orders(manager='active').all().reverse()
    history_orders_button = utils.make_inline_button(
        text=Keys.HISTORY_ORDERS.get(lang),
        CallType=CallTypes.HistoryOrders,
        page=1,
    )
    back_button = utils.make_inline_button(
        text=Keys.BACK.get(lang),
        CallType=CallTypes.Back,
    )
    if not orders.exists():
        order_info = Messages.NO_ACTIVE_ORDERS.get(lang)
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(history_orders_button)
        keyboard.add(back_button)
    else:
        order = orders[page_number-1]
        purchases_info = get_purchases_info(order.purchases.all().reverse(), lang)
        order_info = Messages.ORDER.get(lang).format(
            id=order.id,
            created=utils.datetime_to_utc5_str(order.created),
            updated=utils.datetime_to_utc5_str(order.updated),
            status=order.get_trans_status(lang),
            delivery_type=order.delivery_type,
            purchases_info=purchases_info,
        )
        paginator = Paginator(orders, 1)
        page = paginator.get_page(page_number)
        keyboard = utils.make_page_keyboard(page, CallTypes.Orders)
        keyboard.add(history_orders_button)
        keyboard.add(back_button)

    text = utils.text_to_fat(Keys.ORDERS.get(lang))
    text += utils.text_to_double_line(order_info)
    bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=call.message.id,
        reply_markup=keyboard
    )


def history_orders_call_handler(bot: telebot.TeleBot, call):
    call_type = CallTypes.parse_data(call.data)
    page_number = call_type.page

    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang

    orders = user.orders(manager='finished').all().reverse()
    back_button = utils.make_inline_button(
        text=Keys.BACK.get(lang),
        CallType=CallTypes.Orders,
        page=1,
    )
    if not orders.exists():
        text = Messages.HISTORY_ORDERS_EMPTY.get(lang)
        bot.answer_callback_query(
            callback_query_id=call.id,
            text=text,
            show_alert=True,
        )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button)
        return

    order = orders[page_number-1]
    purchases_info = get_purchases_info(order.purchases.all().reverse(), lang)
    order_info = Messages.ORDER.get(lang).format(
        id=order.id,
        created=utils.datetime_to_utc5_str(order.created),
        updated=utils.datetime_to_utc5_str(order.updated),
        status=order.get_trans_status(lang),
        delivery_type=order.delivery_type,
        purchases_info=purchases_info,
    )
    paginator = Paginator(orders, 1)
    page = paginator.get_page(page_number)
    reorder_button = utils.make_inline_button(
        text=Keys.REORDER.get(lang),
        CallType=CallTypes.ReOrder,
        order_id=order.id,
    )
    keyboard = utils.make_page_keyboard(page, CallTypes.HistoryOrders)
    keyboard.add(reorder_button)
    keyboard.add(back_button)

    text = utils.text_to_fat(Keys.HISTORY_ORDERS.get(lang))
    text += utils.text_to_double_line(order_info)
    bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=call.message.id,
        reply_markup=keyboard
    )


def reorder_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)

    call_type = CallTypes.parse_data(call.data)
    order_id = call_type.order_id
    order = Order.orders.get(id=order_id)
    purchases = order.purchases.all().reverse()

    ordering_start(bot, user, purchases, True, call)
