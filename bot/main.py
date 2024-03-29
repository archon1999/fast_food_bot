import config

import telebot
from telebot import types

from backend.models import BotUser, Order
from backend.templates import Keys, Messages

from bot import products, commands, shopcard, profile, info, orders, admin, statics
from bot.call_types import CallTypes
from bot.states import States


bot = telebot.TeleBot(
    token=config.TOKEN,
    num_threads=3,
    parse_mode='HTML',
)

print(bot.get_me())
message_handlers = {
    '/start': commands.start_command_handler,
    '/menu': commands.menu_command_handler,
}

key_handlers = {
    Keys.MENU: commands.menu_command_handler,
}


@bot.message_handler(content_types=['text'])
def message_handler(message):
    chat_id = message.chat.id
    if BotUser.objects.filter(chat_id=chat_id).exists():
        user = BotUser.objects.get(chat_id=chat_id)
        lang = user.lang
        if (state := user.bot_state):
            if state == States.SEND_CONTACT:
                text = Messages.PLEASE_SEND_CONTACT.get(lang)
                bot.send_message(chat_id, text)

            if state == States.SEND_LOCATION:
                if message.text == Keys.CANCEL.get(lang):
                    user.bot_state = None
                    user.save()
                    commands.menu_command_handler(bot, message)
                else:
                    text = Messages.PLEASE_SEND_LOCATION.get(lang)
                    bot.send_message(chat_id, text)

            if state == States.WRITE_REVIEW:
                user.bot_state = None
                user.save()
                if message.text == Keys.CANCEL.get(lang):
                    commands.menu_command_handler(bot, message)
                else:
                    info.write_review_message_handler(bot, message)

            elif state == States.PROFILE_EDIT_FULL_NAME:
                user.bot_state = None
                user.save()
                profile.profile_edit_full_name(bot, message, user)

            elif state == States.PROFILE_EDIT_CONTACT:
                if (message.text[:5] == '+9989') or (message.text[:4] == '9989'):
                    user.bot_state = None
                    user.save()
                    profile.profile_edit_contact_number(bot, message, user)
                else:
                    text = Messages.PLEASE_CONTACT_NUMBER.get(lang)
                    bot.send_message(chat_id=chat_id, text=text)

            return

    for text, message_handler in message_handlers.items():
        if message.text == text:
            message_handler(bot, message)
            break

    for key, message_handler in key_handlers.items():
        if message.text in key.getall():
            message_handler(bot, message)
            break


callback_query_handlers = {
    CallTypes.Nothing: lambda _, __: True,
    CallTypes.Back: commands.back_call_handler,
    CallTypes.Language: commands.language_call_handler,

    CallTypes.Products: products.products_call_handler,
    CallTypes.Category: products.category_call_handler,
    CallTypes.ProductPage: products.product_page_call_handler,
    CallTypes.PricesProduct: products.add_to_shop_card_call_handler,
    CallTypes.AllProducts: products.all_products_call_handler,

    CallTypes.ShopCard: shopcard.shop_card_call_handler,
    CallTypes.PurchasePage: shopcard.purchase_page_call_handler,
    CallTypes.PurchaseCount: shopcard.purchase_count_call_handler,
    CallTypes.PurchaseRemove: shopcard.purchase_remove_call_handler,
    CallTypes.PurchaseBuy: shopcard.purchase_buy_call_handler,
    CallTypes.PurchasesBuy: shopcard.purchases_buy_call_handler,
    CallTypes.ShopCardYes: shopcard.shop_card_yes_or_no,
    CallTypes.ShopCardCookYes: shopcard.shopcard_cook_call_handler,
    CallTypes.SELFCALL: shopcard.self_call_handler,

    CallTypes.Profile: profile.profile_call_handler,
    CallTypes.ProfileEdit: profile.profile_edit_call_handler,
    CallTypes.ProfileEditFullName: profile.profile_edit_full_name_call_handler,
    CallTypes.ProfileEditContact: profile.profile_edit_contact,

    CallTypes.Info: info.info_call_handler,
    CallTypes.AboutShop: info.about_shop_call_handler,
    CallTypes.ShopContactsAndLocation:
        info.shop_contacts_and_location_call_handler,
    CallTypes.ShopReviews: info.shop_reviews_call_handler,
    CallTypes.ShopMyReview: info.shop_my_review_call_handler,
    CallTypes.ShopMyReviewChange: info.shop_my_review_change_call_handler,
    CallTypes.ShopMyReviewDelete: info.shop_my_review_delete_call_handler,
    CallTypes.ShopMyReviewRatingBall:
        info.shop_my_review_rating_ball_call_handler,
    CallTypes.WantWriteReview: info.want_write_review_call_handler,
    CallTypes.AboutBot: info.about_bot_call_handler,

    CallTypes.Orders: orders.orders_call_handler,
    CallTypes.HistoryOrders: orders.history_orders_call_handler,
    CallTypes.ReOrder: orders.reorder_call_handler,

    CallTypes.Admin: admin.admin_call_handler,
    CallTypes.OnOff: admin.admin_on_off_call_handler,
    CallTypes.CookOnOFF: admin.admin_cook_on_call_handler,
    CallTypes.DriverOnOFF: admin.admin_cook_on_call_handler,

    CallTypes.Statics: statics.statics_all_member,
}


@bot.callback_query_handler(func=lambda _: True)
def callback_query_handler(call):
    call_type = CallTypes.parse_data(call.data)
    chat_id = call.message.chat.id
    if BotUser.objects.filter(chat_id=chat_id).exists():
        user = BotUser.objects.get(chat_id=chat_id)
        if (state := user.bot_state):
            if state == States.CHOOSE_DELIVERY_TYPE:
                if call_type.__class__ == CallTypes.DeliveryType:
                    shopcard.delivery_type_call_handler(bot, call)
            return

    for CallType, query_handler in callback_query_handlers.items():
        if call_type.__class__ == CallType:
            query_handler(bot, call)
            break


@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    if user.bot_state == States.SEND_CONTACT:
        user.full_name = message.chat.first_name
        if message.chat.last_name:
            user.full_name += ' ' + message.chat.last_name

        user.contact = message.contact.phone_number
        user.bot_state = None
        user.full_register = True
        user.save()
        lang = user.lang

        text = Messages.REGISTRATION_FINISHED.get(lang)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                             one_time_keyboard=True)
        keyboard.add(Keys.MENU.get(lang))
        bot.delete_message(chat_id=chat_id, message_id=message.id-1)
        bot.send_message(chat_id, text,
                         reply_markup=keyboard)


@bot.message_handler(content_types=['text', 'location'])
def location_handler(message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    
    if user.bot_state == States.SEND_LOCATION:
        longitude = message.location.longitude
        latitude = message.location.latitude
        order = user.orders.filter(status=Order.Status.RESERVED).first()
        order.longitude = longitude
        order.latitude = latitude
        order.save()

        shopcard.ordering_finish(
            bot=bot,
            user=user,
            message=message,
            delivery_type=Order.DeliveryType.PAYMENT_DELIVERY,
        )


if __name__ == "__main__":
    # bot.polling()
    bot.infinity_polling()
