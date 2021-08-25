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
    YES = keys[18]
    NO = keys[19]
    ABOUT_SHOP = keys[20]
    ABOUT_BOT = keys[21]
    SHOP_CONTACTS_AND_LOCATION = keys[22]
    SHOP_REVIEWS = keys[23]
    MY_REVIEW = keys[24]
    CHANGE_REVIEW = keys[25]
    WRITE_REVIEW = keys[26]
    DELETE_REVIEW = keys[27]
    HISTORY_ORDERS = keys[28]
    REORDER = keys[29]


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
    WANT_WRITE_REVIEW = messages[23]
    ABOUT_SHOP = messages[24]
    REVIEW = messages[25]
    RATING_EVALUATION = messages[26]
    OPINION_MESSAGE = messages[27]
    SAVE_OPINION = messages[28]
    CONTACT_NUMBER = messages[29]
    PLEASE_CONTACT_NUMBER = messages[30]
    SUCCES_CONTACT = messages[31]
    SEND_COOK_AND_DRIVER = messages[32]
    NOT_ACCEPTED_ORDER = messages[33]
    NO_REVIEW = messages[34]
    SHOP_MY_REVIEW_DELETED = messages[35]
    ORDER = messages[36]
    NO_ACTIVE_ORDERS = messages[37]
    HISTORY_ORDERS_EMPTY = messages[38]
    IN_QUEUE = messages[39]
    RESERVED = messages[40]
    PROCESSED = messages[41]
    CANCELED = messages[42]
    COMPLETED = messages[43]
    CASH = messages[44]
    PAYME = messages[45]


class Smiles():
    PREVIOUS = smiles[0]
    NEXT = smiles[1]
    PREVIOUS_5 = smiles[2]
    NEXT_5 = smiles[3]
    ADD = smiles[4]
    SUBTRACT = smiles[5]
    REMOVE = smiles[6]
    STAR = smiles[7]
