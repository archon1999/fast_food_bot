import os

import config

import telebot
from telebot import types
from django.core.paginator import Paginator

from backend.models import BotUser, AboutShop, Review
from backend.templates import Messages, Keys, Smiles

from bot import utils
from bot.call_types import CallTypes


REVIEWS_PER_PAGE = 5


def info_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang

    about_shop_button = utils.make_inline_button(
        text=Keys.ABOUT_SHOP.get(lang),
        CallType=CallTypes.AboutShop,
    )
    about_bot_button = utils.make_inline_button(
        text=Keys.ABOUT_BOT.get(lang),
        CallType=CallTypes.AboutBot,
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(about_shop_button)
    keyboard.add(about_bot_button)

    text = utils.text_to_fat(Keys.INFO.get(lang))
    if call.message.content_type == 'text':
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=call.message.id,
            reply_markup=keyboard,
        )
    elif call.message.content_type == 'photo':
        bot.send_message(chat_id, text,
                         reply_markup=keyboard)
        bot.delete_message(chat_id, call.message.id)


def get_about_shop_info(lang: str):
    about_shop = AboutShop.objects.first()
    text = Messages.ABOUT_SHOP.get(lang).format(
        title=about_shop.get_title(lang),
        description=about_shop.get_description(lang),
    )
    return utils.filter_html(text)


def get_about_shop_image_path():
    about_shop = AboutShop.objects.first()
    if about_shop.image:
        return os.path.join(config.APP_DIR, about_shop.image.name)


def about_shop_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang

    shop_contacts_and_location_button = utils.make_inline_button(
        text=Keys.SHOP_CONTACTS_AND_LOCATION.get(lang),
        CallType=CallTypes.ShopContactsAndLocation,
    )
    shop_reviews_button = utils.make_inline_button(
        text=Keys.SHOP_REVIEWS.get(lang),
        CallType=CallTypes.ShopReviews,
        page=1,
    )
    back_button = utils.make_inline_button(
        text=Keys.BACK.get(lang),
        CallType=CallTypes.Info,
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(shop_contacts_and_location_button)
    keyboard.add(shop_reviews_button)
    keyboard.add(back_button)

    about_shop_info = get_about_shop_info(lang)
    if (image_path := get_about_shop_image_path()):
        with open(image_path, 'rb') as image:
            bot.send_photo(
                chat_id=chat_id,
                photo=image,
                caption=about_shop_info,
                reply_markup=keyboard,
            )
    else:
        bot.edit_message_text(
            text=about_shop_info,
            chat_id=chat_id,
            message_id=call.message.id,
            reply_markup=keyboard,
        )

    bot.delete_message(chat_id, call.message.id)


def about_bot_call_handler(bot: telebot.TeleBot, call):
    pass


def shop_contacts_and_location_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang

    about_shop = AboutShop.objects.first()
    contacts_and_location = utils.filter_html(
        about_shop.get_contacts_and_location(lang)
    )
    bot.send_message(chat_id, contacts_and_location)

    if about_shop.longitude and about_shop.latitude:
        bot.send_location(
            chat_id=chat_id,
            latitude=about_shop.latitude,
            longitude=about_shop.longitude,
        )


def parse_reviews(reviews):
    reviews_info = str()
    for review in reviews:
        rating = f'{Smiles.STAR}'*min(5, review.rating)
        review_info = Messages.REVIEW.text.format(
            full_name=review.user.full_name,
            rating=rating,
            description=review.description,
            datetime=utils.datetime_to_utc5_str(review.updated),
        )
        reviews_info += review_info + '\n\n'

    return reviews_info


def shop_reviews_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang

    call_type = CallTypes.parse_data(call.data)
    page_number = call_type.page
    reviews = Review.reviews.all()
    paginator = Paginator(reviews, REVIEWS_PER_PAGE)
    page = paginator.get_page(page_number)

    my_review_button = utils.make_inline_button(
        text=Keys.MY_REVIEW.get(lang),
        CallType=CallTypes.ShopMyReview,
    )

    text = utils.text_to_fat(Keys.SHOP_REVIEWS.get(lang))
    reviews_info = parse_reviews(page.object_list)
    text += utils.text_to_double_line(reviews_info)

    keyboard = utils.make_page_keyboard(page, CallTypes.ShopReviews)
    keyboard.add(my_review_button)
    if call.message.content_type == 'photo':
        bot.send_message(chat_id, reviews_info,
                         reply_markup=keyboard)
    else:
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=call.message.id,
            reply_markup=keyboard,
        )
