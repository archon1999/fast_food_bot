from datetime import date
import config

import telebot
from telebot import types

from bot import utils
from bot.call_types import CallTypes
from bot.states import States

from backend.models import BotUser, ShopCard
from backend.templates import Messages, Keys


def start_command_handler(bot: telebot.TeleBot, message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()

    uz_language_button = utils.make_inline_button(
        text=Keys.LANGUAGE.get(BotUser.Lang.UZ),
        CallType=CallTypes.Language,
        lang=BotUser.Lang.UZ,
    )
    ru_language_button = utils.make_inline_button(
        text=Keys.LANGUAGE.get(BotUser.Lang.RU),
        CallType=CallTypes.Language,
        lang=BotUser.Lang.RU,
    )
    en_language_button = utils.make_inline_button(
        text=Keys.LANGUAGE.get(BotUser.Lang.EN),
        CallType=CallTypes.Language,
        lang=BotUser.Lang.EN,
    )

    keyboard.add(uz_language_button)
    keyboard.add(ru_language_button)
    keyboard.add(en_language_button)

    text = Messages.START_COMMAND_HANDLER.text
    bot.send_message(chat_id, text,
                     reply_markup=keyboard)


def language_call_handler(bot: telebot.TeleBot, call):
    call_type = CallTypes.parse_data(call.data)
    lang = call_type.lang
    chat_id = call.message.chat.id
    user, success = BotUser.objects.get_or_create(chat_id=chat_id)
    user.lang = lang
    user.save()
    ShopCard.shop_cards.get_or_create(user=user)
    if success:
        ShopCard.shop_cards.create(user=user)
        registration_start_handler(bot, call.message)
    else:
        menu_command_handler(bot, call.message)


def registration_start_handler(bot: telebot.TeleBot, message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang
    user.bot_state = States.SEND_CONTACT
    user.save()
    text = Messages.REGISTRATION_INFO.get(lang)
    contact_button = types.KeyboardButton(
        text=Keys.SEND_CONTACT.get(lang),
        request_contact=True
    )
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(contact_button)

    bot.send_message(chat_id, text,
                     reply_markup=keyboard)


def menu_command_handler(bot: telebot.TeleBot, message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang
    products_button = utils.make_inline_button(
        text=Keys.PRODUCTS.get(lang),
        CallType=CallTypes.Products,
    )
    shop_card_button = utils.make_inline_button(
        text=Keys.SHOP_CARD.get(lang),
        CallType=CallTypes.ShopCard,
    )
    orders_button = utils.make_inline_button(
        text=Keys.ORDERS.get(lang),
        CallType=CallTypes.Orders,
    )
    profile_button = utils.make_inline_button(
        text=Keys.PROFILE.get(lang),
        CallType=CallTypes.Profile,
    )
    info_button = utils.make_inline_button(
        text=Keys.INFO.get(lang),
        CallType=CallTypes.Info,
    )

    menu_keyboard = types.InlineKeyboardMarkup()
    menu_keyboard.add(products_button, shop_card_button)
    menu_keyboard.add(orders_button, profile_button)
    menu_keyboard.add(info_button)
    if user.type == BotUser.Type.ADMIN:
        admin_button = utils.make_inline_button(
            text=Keys.ADMIN.get(lang),
            CallType=CallTypes.Admin,
        )
        menu_keyboard.add(admin_button)
    bot.delete_message(chat_id=chat_id, message_id=message.id)
    text = Messages.MENU.get(lang)
    if hasattr(message, 'edited'):
        bot.edit_message_text(
            chat_id=chat_id,
            text=text,
            message_id=message.id,
            reply_markup=menu_keyboard,
        )
    else:
        bot.send_message(chat_id, text,
                         reply_markup=menu_keyboard)


def back_call_handler(bot: telebot.TeleBot, call):
    call.message.edited = True
    menu_command_handler(bot, call.message)
