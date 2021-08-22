from .models import Template


keys = Template.keys.all()
messages = Template.messages.all()
smiles = Template.smiles.all()


class Keys():
    SEND_CONTACT = keys[0]
    LANGUAGE = keys[1]
    PRODUCTS = keys[2]
    SHOP_CARD = keys[3]
    ORDERS = keys[4]
    PROFILE = keys[5]
    BACK = keys[6]
    ALL_PRODUCTS = keys[7]
    ADD_TO_SHOP_CARD = keys[8]
    MENU = keys[9]
    INFO = keys[10]
    ADMIN = keys[11]
    VIEW_PURCHASES = keys[12]
    SEND_LOCATION = keys[13]
    CANCEL = keys[14]
    PAYMENT_DELIVERY = keys[15]
    SELF_CALL = keys[16]
    PROFILE_EDIT = keys[17]
    YES_KEYBOARD = keys[18]
    NO_KEYBOARD = keys[19]
    ABOUT_SHOP = keys[20]
    ABOUT_BOT = keys[21]
    SHOP_CONTACTS_AND_LOCATION = keys[22]
    SHOP_REVIEWS = keys[23]
    MY_REVIEW = keys[24]


class Messages():
    START_COMMAND_HANDLER = messages[0]
    REGISTRATION_INFO = messages[1]
    MENU = messages[2]
    CHOOSE_CATEGORY = messages[3]
    PRODUCT_INFO = messages[4]
    ADDED_TO_SHOP_CARD = messages[5]
    SHOP_CARD_INFO = messages[6]
    REGISTRATION_FINISHED = messages[7]
    BUY_ONE = messages[8]
    BUY_ALL = messages[9]
    EMPTY_SHOP_CARD = messages[10]
    PURCHASES_INFO = messages[11]
    PURCHASE_INFO = messages[12]
    PLEASE_SEND_CONTACT = messages[13]
    SEND_LOCATION = messages[14]
    CHOOSE_DELIVERY_TYPE = messages[15]
    PLEASE_SEND_LOCATION = messages[16]
    PROFILE_INFO = messages[17]
    SUCCESFULL_ORDERING = messages[18]
    NEW_ORDER = messages[19]
    PROFILE_EDIT = messages[20]
    PROFILE_EDIT_FULLNAME = messages[21]
    SUCCES_FULL_NAME = messages[22]
    RATING_MESSAGE = messages[23]
    ABOUT_SHOP = messages[24]
    REVIEW = messages[25]


class Smiles():
    PREVIOUS = smiles[0]
    NEXT = smiles[1]
    PREVIOUS_5 = smiles[2]
    NEXT_5 = smiles[3]
    ADD = smiles[4]
    SUBTRACT = smiles[5]
    REMOVE = smiles[6]
    STAR = smiles[7]
