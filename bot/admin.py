from bot.states import States
from telebot import util
import config

import telebot
from telebot import types

from backend.models import BotUser, Order, AdminPanel
from backend.templates import Messages, Smiles, Keys
from bot import utils
from bot.call_types import CallTypes

def admin_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang
    button = [
        utils.make_inline_button(
            text=Keys.ON_OFF.get(lang),
            CallType=CallTypes.OnOff
        ),
        utils.make_inline_button(
            text=Keys.STATISTIKA.get(lang),
            CallType=CallTypes.Statics
        ),
        utils.make_inline_button(
            text=Keys.ORDERS.get(lang),
            CallType=CallTypes.OrderAdmin
        ),
    ]
    back_button = utils.make_inline_button(
        text=Keys.BACK.get(lang),
        CallType=CallTypes.Back,
    )
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*button)
    keyboard.add(back_button)
    text = Messages.ADMIN_MENU.get(lang)
    bot.edit_message_text(text=text, chat_id=chat_id,
                            message_id=call.message.id, reply_markup=keyboard)

def admin_on_off_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    
    cook = Messages.OFF.get(user.lang)
    driver = Messages.OFF.get(user.lang)
    panel = AdminPanel.objects.get(id=1)
    
    cook_button = [
        utils.make_inline_button(
            text=Keys.COOK.get(user.lang),
            CallType=CallTypes.Nothing
        ),
        utils.make_inline_button(
            text=Keys.ON.get(user.lang),
            CallType=CallTypes.CookOnOFF,
            id=1
        )
    ]
    
    driver_button = [
        utils.make_inline_button(
            text=Keys.DRIVER.get(user.lang),
            CallType=CallTypes.Nothing
        ),
        utils.make_inline_button(
            text=Keys.ON.get(user.lang),
            CallType=CallTypes.DriverOnOFF,
            id=1
        )
    ]
    
    if panel.cook == States.COOK:
        cook = Messages.ON.get(user.lang)
        cook_button = [
            utils.make_inline_button(
                text=Keys.COOK.get(user.lang),
                CallType=CallTypes.Nothing
            ),
            utils.make_inline_button(
                text=Keys.OFF.get(user.lang),
                CallType=CallTypes.CookOnOFF,
                id=0
            )
        ]
    
        if panel.driver == States.DRIVER:
            print(2)
            driver = Messages.ON.get(user.lang)
            driver_button = [
                utils.make_inline_button(
                    text=Keys.DRIVER.get(user.lang),
                    CallType=CallTypes.Nothing
                ),
                utils.make_inline_button(
                    text=Keys.OFF.get(user.lang),
                    CallType=CallTypes.DriverOnOFF,
                    id=0
                )
            ]
    
    back_button = utils.make_inline_button(
        text=Keys.BACK.get(user.lang),
        CallType=CallTypes.Admin,
    )
    
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*cook_button, *driver_button, back_button)
    text = Messages.ADMIN_ON_OF_CALL.get(user.lang).format(
        cook=cook,
        driver=driver)

    bot.edit_message_text(text=text, chat_id=chat_id,
                            message_id=call.message.id, reply_markup=keyboard)

def admin_cook_on_call_handler(bot: telebot.TeleBot, call):
    call_type = CallTypes.parse_data(call.data)
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    panel = AdminPanel.objects.get(id=1)
    if call_type.id == 1:
        panel.cook = States.COOK
        panel.save()
        text = Messages.CHANGE.get(user.lang)
        bot.answer_callback_query(callback_query_id=call.id, text=text,
                                    show_alert=True)
        admin_on_off_call_handler(bot=bot, call=call)
    else:
        panel.cook = ''
        panel.save()
        text = Messages.CHANGE.get(user.lang)
        bot.answer_callback_query(callback_query_id=call.id, text=text,
                                    show_alert=True)
        admin_on_off_call_handler(bot=bot, call=call)