import os
import config

import telebot
from telebot import types

from backend.models import BotUser, Product, Order, AdminPanel, AboutShop
from backend.templates import Messages, Smiles, Keys

from bot import utils, commands
from bot.call_types import CallTypes
from bot.states import States


    
def get_purchases_info(purchases, lang):
    all_purchases_info = str()
    purchases_price = 0
    print(purchases.count())
    for purchase in purchases:
        purchase_info = Messages.PURCHASE_INFO.get(lang).format(
            product_title=purchase.product.get_title(lang),
            count=purchase.count,
            price=purchase.price,
        )
        print(purchase_info)
        purchases_price += purchase.price
        all_purchases_info += purchase_info + '\n'

    purchases_info = Messages.PURCHASES_INFO.get(lang).format(
        all_purchases_info=all_purchases_info,
        purchases_price=purchases_price,
    )
    print('------------------')
    return purchases_info


def shop_card_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang
    shop_card = user.shop_card
    purchases = shop_card.purchases.all()
    purchases_count = purchases.count()
    if purchases_count == 0:
        bot.answer_callback_query(
            callback_query_id=call.id,
            text=Messages.EMPTY_SHOP_CARD.get(lang),
            show_alert=True,
        )
        return

    text = get_purchases_info(purchases, lang)
    view_purchases_button = utils.make_inline_button(
        text=Keys.VIEW_PURCHASES.get(lang),
        CallType=CallTypes.PurchasePage,
        page=0,
    )
    price_all = shop_card.price
    buy_all_button = utils.make_inline_button(
        text=Messages.BUY_ALL.get(lang).format(price_all=price_all),
        CallType=CallTypes.PurchasesBuy,
    )
    back_button = utils.make_inline_button(
        text=Keys.BACK.get(lang),
        CallType=CallTypes.Back,
    )

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(view_purchases_button)
    keyboard.add(buy_all_button)
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


def get_product_info(product: Product, lang: str):
    return Messages.PRODUCT_INFO.get(lang).format(
        id=product.id,
        title=product.get_title(lang),
        price=product.price,
        description=product.get_description(lang),
        category_title=product.category.get_name(lang),
    )


def get_product_image_path(product: Product):
    return os.path.join(config.APP_DIR, product.image.name)


def make_purchase_keyboard(user: BotUser, page):
    shop_card = user.shop_card
    purchases = shop_card.purchases.all()
    purchases_count = purchases.count()
    purchase = purchases[page]
    lang = user.lang
    page_buttons = [
        utils.make_inline_button(
            text=Smiles.PREVIOUS.text,
            CallType=CallTypes.PurchasePage,
            page=utils.normalize_page(page-1, purchases_count),
        ),
        utils.make_inline_button(
            text=str(page+1),
            CallType=CallTypes.Nothing,
        ),
        utils.make_inline_button(
            text=Smiles.NEXT.text,
            CallType=CallTypes.PurchasePage,
            page=utils.normalize_page(page+1, purchases_count),
        ),
    ]
    plus_minus_buttons = [
        utils.make_inline_button(
            text=Smiles.SUBTRACT.text,
            CallType=CallTypes.PurchaseCount,
            page=page,
            count=purchase.count-1,
        ),
        utils.make_inline_button(
            text=str(purchase.count),
            CallType=CallTypes.Nothing,
        ),
        utils.make_inline_button(
            text=Smiles.ADD.text,
            CallType=CallTypes.PurchaseCount,
            page=page,
            count=purchase.count+1,
        ),
    ]

    remove_button = utils.make_inline_button(
        text=Smiles.REMOVE.text,
        CallType=CallTypes.PurchaseRemove,
        page=page,
    )

    price_one = purchase.price
    buy_one_button = utils.make_inline_button(
        text=Messages.BUY_ONE.get(lang).format(price_one=price_one),
        CallType=CallTypes.PurchaseBuy,
        page=page,
    )

    price_all = shop_card.price
    buy_all_button = utils.make_inline_button(
        text=Messages.BUY_ALL.get(lang).format(price_all=price_all),
        CallType=CallTypes.PurchasesBuy,
    )

    keyboard = types.InlineKeyboardMarkup(row_width=5)
    keyboard.add(*page_buttons)
    keyboard.add(*plus_minus_buttons)
    keyboard.add(remove_button)
    keyboard.add(buy_one_button)
    keyboard.add(buy_all_button)
    return keyboard


def purchase_page_call_handler(bot: telebot.TeleBot, call):
    call_type = CallTypes.parse_data(call.data)
    page = call_type.page

    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang

    shop_card = user.shop_card
    purchases = shop_card.purchases.all()
    try:
        purchase = purchases[page]
    except IndexError:
        bot.answer_callback_query(
            callback_query_id=call.id,
            text=Messages.EMPTY_SHOP_CARD.get(lang),
            show_alert=True,
        )
        return

    product = purchase.product

    product_info = get_product_info(product, lang)
    image_path = get_product_image_path(product)
    keyboard = make_purchase_keyboard(user, page)

    with open(image_path, 'rb') as photo:
        if call.message.content_type == 'photo':
            bot.edit_message_media(
                media=types.InputMedia(
                    type='photo',
                    media=photo,
                    caption=product_info,
                    parse_mode='HTML',
                ),
                chat_id=chat_id,
                message_id=call.message.id,
                reply_markup=keyboard,
            )
        else:
            bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=product_info,
                reply_markup=keyboard,
            )


def purchase_count_call_handler(bot: telebot.TeleBot, call):
    call_type = CallTypes.parse_data(call.data)
    page = call_type.page
    count = call_type.count
    if count == 0:
        call_type = CallTypes.PurchaseRemove(page=page)
        call.data = CallTypes.make_data(call_type)
        purchase_remove_call_handler(bot, call)
        return

    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)

    shop_card = user.shop_card
    purchases = shop_card.purchases.all()
    purchase = purchases[page]
    purchase.count = count
    purchase.save()

    call_type = CallTypes.PurchasePage(page=page)
    call.data = CallTypes.make_data(call_type)
    purchase_page_call_handler(bot, call)


def purchase_remove_call_handler(bot: telebot.TeleBot, call):
    call_type = CallTypes.parse_data(call.data)
    page = call_type.page

    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)

    shop_card = user.shop_card
    purchases = shop_card.purchases.all()
    purchase = purchases[page]
    purchase.delete()

    call_type = CallTypes.PurchasePage(page=page)
    call.data = CallTypes.make_data(call_type)
    purchase_page_call_handler(bot, call)


def ordering_start(bot: telebot.TeleBot, user: BotUser, purchases, reorder):
    order = Order.orders.create(
        user=user,
        status=Order.Status.RESERVED,
    )
    order.purchases.set(purchases)
    panel = AdminPanel.objects.get(id=1)

    if not reorder:
        for purchase in purchases:
            user.shop_card.purchases.remove(purchase)

    chat_id = user.chat_id
    lang = user.lang

    user.bot_state = States.CHOOSE_DELIVERY_TYPE
    user.save()

    self_call_button = utils.make_inline_button(
        text=Keys.SELF_CALL.get(lang),
        CallType=CallTypes.DeliveryType,
        delivery_type=Order.DeliveryType.SELF_CALL,
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(self_call_button)

    if panel.driver == States.DRIVER:
        payment_delivery_button = utils.make_inline_button(
            text=Keys.PAYMENT_DELIVERY.get(lang),
            CallType=CallTypes.DeliveryType,
            delivery_type=Order.DeliveryType.PAYMENT_DELIVERY,
        )
        keyboard.add(payment_delivery_button)
    text = Messages.CHOOSE_DELIVERY_TYPE.get(lang)
    bot.send_message(chat_id, text,
                     reply_markup=keyboard)


def purchase_buy_call_handler(bot: telebot.TeleBot, call):
    call_type = CallTypes.parse_data(call.data)
    page = call_type.page

    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)

    shop_card = user.shop_card
    purchases = shop_card.purchases.all()
    purchase = purchases[page]
    purchases = shop_card.purchases.filter(id=purchase.id)
    ordering_start(bot, user, purchases, False)


def purchases_buy_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)

    shop_card = user.shop_card
    purchases = shop_card.purchases.all()
    ordering_start(bot, user, purchases, False)


def delivery_type_call_handler(bot: telebot.TeleBot, call):
    call_type = CallTypes.parse_data(call.data)
    delivery_type = call_type.delivery_type

    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang

    if delivery_type == Order.DeliveryType.PAYMENT_DELIVERY:
        text = Messages.SEND_LOCATION.get(lang)
        user.bot_state = States.SEND_LOCATION
        user.save()
        send_location_button = types.KeyboardButton(
            text=Keys.SEND_LOCATION.get(lang),
            request_location=True,
        )
        keyboard = types.ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True,
        )
        keyboard.add(send_location_button)
        keyboard.add(Keys.CANCEL.get(lang))
        bot.send_message(chat_id, text,
                         reply_markup=keyboard)
    else:
        ordering_finish(bot, user, call.message, delivery_type)


def yes_or_no(id, admins):
    panel = AdminPanel.objects.get(id=1)
    if panel.cook == States.COOK:
        button = [
            utils.make_inline_button(
                text=Keys.YES.get(admins.lang),
                CallType=CallTypes.ShopCardYes,
                id=id,
                yes='yes',
            ),
            utils.make_inline_button(
                text=Keys.NO.get(admins.lang),
                CallType=CallTypes.ShopCardYes,
                id=id,
                yes='no',
            )
        ]
    else:
        button = [
            utils.make_inline_button(
                text=Keys.YES.get(admins.lang),
                CallType=CallTypes.ShopCardCookYes,
                id=id,
                yes='yes',
            ),
            utils.make_inline_button(
                text=Keys.NO.get(admins.lang),
                CallType=CallTypes.ShopCardCookYes,
                id=id,
                yes='no',
            )
        ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*button)
    return keyboard

def self_call_keyboard(id, lang):
    button = [
        utils.make_inline_button(
            text=Keys.YES.get(lang),
            CallType=CallTypes.SELFCALL,
            id=id,
            yes='yes'
        ),
        utils.make_inline_button(
            text=Keys.NO.get(lang),
            CallType=CallTypes.SELFCALL,
            id=id,
            yes='no'
        )
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*button)
    return keyboard

def ordering_finish(bot: telebot.TeleBot, user, message, delivery_type):
    order = user.orders.filter(status=Order.Status.RESERVED).first()
    order.delivery_type = delivery_type
    order.status = Order.Status.IN_QUEUE
    order.save()
    user.bot_state = None
    user.save()

    text = Messages.SUCCESFULL_ORDERING.get(user.lang).format(id=order.id)
    bot.send_message(chat_id=user.chat_id, text=text)
    commands.menu_command_handler(bot=bot, message=message)
    for admin in BotUser.admins.all():
        if order.delivery_type == Order.DeliveryType.PAYMENT_DELIVERY:
            shop_card = user.shop_card
            purchases = shop_card.purchases.all()
            text = get_purchases_info(purchases, user.lang)
            print(text)
            print('--------------------------------')

            bot.send_location(
                chat_id=admin.chat_id,
                latitude=order.latitude,
                longitude=order.longitude
            )
            text = Messages.NEW_ORDER.get(user.lang).format(
                id=order.id,
                uid=user.chat_id,
                user=user,
                contact=user.contact,
                delivery_type=order.get_trans_status(user.lang),
                text=text
            )

            bot.send_message(
                chat_id=admin.chat_id,
                text=text,
                reply_markup=yes_or_no(order.id, admin)
            )
        else:

            text = Messages.NEW_ORDER.get(user.lang).format(
                id=order.id,
                uid=user.chat_id,
                user=user,
                contact=user.contact,
                delivery_type=order.get_trans_delivery_type(user.lang),
            )
            bot.send_message(
                chat_id=admin.chat_id,
                text=text,
                reply_markup=self_call_keyboard(order.id, user.lang)
            )
            
def cook_keyboard(id, cook):
    button = [
        utils.make_inline_button(
            text=Keys.YES.get(cook.lang),
            CallType=CallTypes.ShopCardCookYes,
            id=id,
            yes='yes',
        ),
        utils.make_inline_button(
            text=Keys.NO.get(cook.lang),
            CallType=CallTypes.ShopCardCookYes,
            id=id,
            yes='no',
        )
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*button)
    return keyboard

def shop_card_yes_or_no(bot: telebot.TeleBot, call):
    call_type = CallTypes.parse_data(call.data)
    chat_id = call.message.chat.id
    order = Order.orders.get(id=call_type.id)
    user= BotUser.objects.get(chat_id=chat_id)
    if call_type.yes == 'yes':
        order = Order.orders.get(id=call_type.id)
        order.status = Order.Status.PROCESSED
        order.save()
        text = Messages.SEND_COOK_AND_DRIVER.get(user.lang).format(id=call_type.id)
        bot.send_message(chat_id=chat_id, text=text)
        commands.menu_command_handler(bot, call.message)
        for cook in BotUser.objects.filter(type=BotUser.Type.COOK):
                text = Messages.NEW_ORDER.get(cook.lang).format(
                    id=call_type.id,
                    uid=order.user.chat_id, 
                    user=order.user, 
                    contact=order.user.contact,
                    delivery_type=order.get_trans_status(cook.lang),
                    longitude=order.longitude,
                    latitude=order.latitude, 
                )

                bot.send_message(chat_id=cook.chat_id, text=text, 
                                    reply_markup=cook_keyboard(call_type.id, cook))

    else:
        order = Order.orders.get(id=call_type.id)
        order.status = order.get_trans_status(user.lang)
        order.save()
        text = Messages.NOT_ACCEPTED_ORDER.get(order.user.lang).format(id=call_type.id)
        bot.delete_message(chat_id=chat_id, message_id=call.message.id-1)
        bot.delete_message(chat_id=chat_id, message_id=call.message.id)
        bot.send_message(chat_id=order.user.chat_id, text=text)
        commands.menu_command_handler(bot, call.message)
        
         
def shopcard_cook_call_handler(bot: telebot.TeleBot, call):
    call_type = CallTypes.parse_data(call.data)
    chat_id = call.message.chat.id
    order = Order.orders.get(id=call_type.id)
    user= BotUser.objects.get(chat_id=chat_id)
    print(call_type)
    if call_type.yes == 'yes':
        order = Order.orders.get(id=call_type.id)
        order.status = Order.Status.COMPLETED
        order.save()
        text = Messages.SEND_COOK_AND_DRIVER.get(user.lang).format(id=call_type.id)
        bot.send_message(chat_id=chat_id, text=text)
        commands.menu_command_handler(bot, call.message)
        for driver in BotUser.objects.filter(type=BotUser.Type.DRIVER):
                text = Messages.NEW_ORDER.get(driver.lang).format(
                    id=call_type.id,
                    uid=order.user.chat_id, 
                    user=order.user, 
                    contact=order.user.contact,
                    delivery_type=order.get_trans_status(driver.lang),
                    longitude=order.longitude,
                    latitude=order.latitude, 
                )

                bot.send_message(chat_id=driver.chat_id, text=text, )
                                    # reply_markup=cook_keyboard(call_type.id, cook))
                
                bot.send_location(chat_id=driver.chat_id, latitude=order.latitude,
                                        longitude=order.longitude)
    else:
        text = Messages.NOT_ACCEPTED_ORDER.get(order.user.lang).format(id=call_type.id)
        bot.send_message(chat_id=order.user.chat_id, text=text)
        commands.menu_command_handler(bot, call.message)
         