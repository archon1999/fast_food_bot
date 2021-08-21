import os
from backend.admin import CategoryAdmin
import config

import telebot
from telebot import types

from backend.models import BotUser, Info
from backend.templates import Messages, Keys

from bot import utils
from bot.call_types import CallTypes

def get_info_image_path(info: Info):
    return os.path.join(config.APP_DIR, info.image.name)


def get_info_info(info: Info, lang: str):

    return Messages.INFO_MESSAGE.get(lang).format(
        title=info.get_title(lang),
        description=info.get_description(lang),
    )

def get_button(info: Info, lang):
    button = []
    for inf in info.comments.all():
        button.append(types.InlineKeyboardButton(
            text=inf.name,
            callback_data=inf.name1
        ))
    back_button =   utils.make_inline_button(
        text=Keys.BACK.get(lang),
        CallType=CallTypes.Back,
    )
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*button)
    keyboard.add(back_button)
    return keyboard

    
def info_message_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    info = Info.objects.get(id=1)
    keyboard = get_button(info, user.lang)
    image_path = get_info_image_path(info)
    product_info = get_info_info(info, user.lang)
    with open(image_path, 'rb') as photo:
        # bot.edit_message_media(
        #     media=types.InputMedia(
        #         type='photo',
        #         media=photo,
        #         caption=product_info,
        #         parse_mode='HTML',
        #     ),
        #     chat_id=chat_id,
        #     message_id=call.message.id,
        #     # reply_markup=keyboard,
        # )
        bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=product_info,
            reply_markup=keyboard
        )



# for info in Info.objects.all():
#     print(info.title_uz, info.description_uz)
#     for i in info.comments.all():
#         print(i.name, i.name1)