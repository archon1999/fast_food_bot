import os

import config

import telebot
from telebot import types
from django.core.paginator import Paginator

from backend.models import BotUser, AboutShop, Review, AboutBot
from backend.templates import Messages, Keys, Smiles

from bot.states import States
from bot import utils, commands
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
    back_button = utils.make_inline_button(
        text=Keys.BACK.get(user.lang),
        CallType=CallTypes.Back,
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(about_shop_button)
    keyboard.add(about_bot_button)
    keyboard.add(back_button)
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
    back_button = utils.make_inline_button(
        text=Keys.BACK.get(lang),
        CallType=CallTypes.Back,
    )
    text = utils.text_to_fat(Keys.SHOP_REVIEWS.get(lang))
    reviews_info = parse_reviews(page.object_list)
    text += utils.text_to_double_line(reviews_info)

    keyboard = utils.make_page_keyboard(page, CallTypes.ShopReviews)
    keyboard.add(my_review_button)
    keyboard.add(back_button)
    if call.message.content_type == 'photo':
        bot.send_message(chat_id, text,
                         reply_markup=keyboard)
    else:
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=call.message.id,
            reply_markup=keyboard,
        )


def shop_my_review_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang

    keyboard = types.InlineKeyboardMarkup()
    if Review.reviews.filter(user=user).exists():
        my_review = user.shop_review
        rating = f'{Smiles.STAR}'*min(5, my_review.rating)
        my_review_info = Messages.REVIEW.get(lang).format(
            full_name=user.full_name,
            rating=rating,
            description=my_review.description,
            datetime=utils.datetime_to_utc5_str(my_review.updated),
        ) + '\n'
        change_review_button = utils.make_inline_button(
            text=Keys.CHANGE_REVIEW.get(lang),
            CallType=CallTypes.ShopMyReviewChange,
        )
        delete_review_button = utils.make_inline_button(
            text=Keys.DELETE_REVIEW.get(lang),
            CallType=CallTypes.ShopMyReviewDelete,
        )
        keyboard.add(change_review_button)
        keyboard.add(delete_review_button)
    else:
        my_review_info = Messages.NO_REVIEW.get(lang)
        write_review_button = utils.make_inline_button(
            text=Keys.WRITE_REVIEW.get(lang),
            CallType=CallTypes.ShopMyReviewChange,
        )
        keyboard.add(write_review_button)

    text = utils.text_to_fat(Keys.MY_REVIEW)
    text += utils.text_to_double_line(my_review_info)
    back_button = utils.make_inline_button(
        text=Keys.BACK.get(lang),
        CallType=CallTypes.ShopReviews,
        page=1,
    )
    keyboard.add(back_button)

    bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=call.message.id,
        reply_markup=keyboard,
    )


def make_review_rating_keyboard(lang):
    max_rating = 5
    min_rating = 1
    keyboard = types.InlineKeyboardMarkup()
    for rating_ball in reversed(range(min_rating, max_rating+1)):
        rating_star_button = utils.make_inline_button(
            text=f'{Smiles.STAR}'*rating_ball,
            CallType=CallTypes.ShopMyReviewRatingBall,
            ball=rating_ball,
        )
        keyboard.add(rating_star_button)

    back_button = utils.make_inline_button(
        text=Keys.BACK.get(lang),
        CallType=CallTypes.ShopMyReview,
    )
    keyboard.add(back_button)
    return keyboard


def shop_my_review_change_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang
    text = Messages.RATING_EVALUATION.get(lang)
    keyboard = make_review_rating_keyboard(lang)
    bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=call.message.id,
        reply_markup=keyboard
    )


def shop_my_review_delete_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    user.shop_review.delete()
    lang = user.lang
    text = Messages.SHOP_MY_REVIEW_DELETED.get(lang)
    bot.send_message(chat_id, text)
    commands.menu_command_handler(bot, call.message)


def shop_my_review_rating_ball_call_handler(bot: telebot.TeleBot, call):
    call_type = CallTypes.parse_data(call.data)
    ball = call_type.ball

    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang

    if Review.reviews.filter(user=user).exists():
        review = Review.reviews.get(user=user)
        review.description = str()
    else:
        review = Review.reviews.create(user=user, rating=ball)

    review.save()
    text = Messages.WANT_WRITE_REVIEW.get(user.lang)
    want_write_review_yes_button = utils.make_inline_button(
        text=Keys.YES.get(lang),
        CallType=CallTypes.WantWriteReview,
        flag=True,
    )
    want_write_review_no_button = utils.make_inline_button(
        text=Keys.NO.get(lang),
        CallType=CallTypes.WantWriteReview,
        flag=False,
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(want_write_review_yes_button)
    keyboard.add(want_write_review_no_button)
    bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=call.message.id,
        reply_markup=keyboard,
    )


def want_write_review_call_handler(bot: telebot.TeleBot, call):
    call_type = CallTypes.parse_data(call.data)
    flag = call_type.flag

    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang

    if flag:
        text = Messages.OPINION_MESSAGE.get(lang)
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=call.message.id,
        )
        user.bot_state = States.WRITE_REVIEW
        user.save()
    else:
        commands.back_call_handler(bot, call)


def write_review_message_handler(bot: telebot.TeleBot, message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)

    review = user.shop_review
    review.description = message.text
    review.save()

    text = Messages.SAVE_OPINION.get(user.lang)
    bot.send_message(chat_id, text)
    commands.menu_command_handler(bot, message)


def get_about_bot_info(lang: str):
    aboutbot = AboutBot.objects.first()
    text = Messages.ABOUT_SHOP.get(lang).format(
        title=aboutbot.get_title(lang),
        description=aboutbot.get_description(lang),
    )
    return utils.filter_html(text)


def about_bot_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang
    back_button = utils.make_inline_button(
        text=Keys.BACK.get(lang),
        CallType=CallTypes.Back,
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(back_button)
    text = get_about_bot_info(lang)
    bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=call.message.id,
        disable_web_page_preview=True,
        reply_markup=keyboard
    )
