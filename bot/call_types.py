class CallTypeMeta(type):
    def __new__(cls, name, *args):
        def __init__(self, **kwargs):
            assert(len(args) == len(kwargs))
            for arg in args:
                if arg.endswith('__int'):
                    suffix_removed_arg = arg.removesuffix('__int')
                    value = int(kwargs[suffix_removed_arg])
                    setattr(self, suffix_removed_arg, value)
                elif arg.endswith('__list'):
                    suffix_removed_arg = arg.removesuffix('__list')
                    value = '#'.join(map(str, kwargs[suffix_removed_arg]))
                    setattr(self, suffix_removed_arg, value)
                else:
                    setattr(self, arg, kwargs[arg])

        def __str__(self):
            args = {
                CallTypes.CLASS_NAME: self.__class__.__name__,
            } | self.__dict__
            return str(args)

        CallType = type(name, (), {})
        CallType.__init__ = __init__
        CallType.__str__ = __str__
        return CallType


class CallTypes():
    ARGS_SEP = '|'
    ARG_SEP = ':'
    VALUES_SEP = '#'
    CLASS_NAME = 'type'

    Menu = CallTypeMeta('Menu')
    Back = CallTypeMeta('Back')
    Language = CallTypeMeta('Language', 'lang')

    Products = CallTypeMeta('Products')
    ShopCard = CallTypeMeta('ShopCard')
    Orders = CallTypeMeta('Orders', 'page__int')
    Profile = CallTypeMeta('Profile')
    Info = CallTypeMeta('Info')
    Admin = CallTypeMeta('Admin')

    Category = CallTypeMeta('Category', 'category_id__int')
    AllProducts = CallTypeMeta('AllProducts', 'category_id__int')
    ProductPage = CallTypeMeta('ProductPage', 'category_id__int',
                               'page__int')
    AddToShopCard = CallTypeMeta('AddToShopCard', 'product_id__int')
    PricesProduct = CallTypeMeta('PricesProduct', 'product_id__int', 'price__int')
    PurchasePage = CallTypeMeta('PurchasePage', 'page__int')
    PurchaseCount = CallTypeMeta('PurchaseCount', 'page__int', 'count__int')
    PurchaseRemove = CallTypeMeta('PurchaseRemove', 'page__int')
    PurchaseBuy = CallTypeMeta('PurchaseBuy', 'page__int')
    PurchasesBuy = CallTypeMeta('PurchasesBuy')
    ShopCardYes = CallTypeMeta('ShopCardYes', 'id__int', 'yes',)
    ShopCardDriver = CallTypeMeta('ShopCardDriver', 'id__int')
    ShopCardCookYes = CallTypeMeta('ShopCardCookYes', 'id__int', 'yes')
    DeliveryType = CallTypeMeta('DeliveryType', 'delivery_type')
    SELFCALL = CallTypeMeta('SELFCALL', 'id__int', 'yes')
    ProfileEdit = CallTypeMeta('ProfileEdit')
    ProfileEditFullName = CallTypeMeta('ProfileEditFullName')
    ProfileEditContact = CallTypeMeta('ProfileEditContact')

    AboutShop = CallTypeMeta('AboutShop')
    ShopContactsAndLocation = CallTypeMeta('ShopContactsAndLocation')
    ShopReviews = CallTypeMeta('ShopReviews', 'page__int')
    ShopMyReview = CallTypeMeta('ShopMyReview')
    ShopMyReviewChange = CallTypeMeta('ShopMyReviewChange')
    ShopMyReviewDelete = CallTypeMeta('ShopMyReviewDelete')
    ShopMyReviewRatingBall = CallTypeMeta('ShopMyReviewRatingBall',
                                          'ball__int')
    WantWriteReview = CallTypeMeta('WantWriteReview', 'flag__int')
    AboutBot = CallTypeMeta('AboutBot')

    HistoryOrders = CallTypeMeta('HistoryOrders', 'page__int')
    ReOrder = CallTypeMeta('ReOrder', 'order_id__int')

    OnOff = CallTypeMeta('OnOff')
    Statics = CallTypeMeta('Statics')
    OrderAdmin = CallTypeMeta('OrderAdmin')

    CookOnOFF = CallTypeMeta('CookOnOFF', 'id__int', 'status', 'difference')
    DriverOnOFF = CallTypeMeta('DriverOnOFF', 'id__int', 'status', 'difference')



    Nothing = CallTypeMeta('Nothing')

    @classmethod
    def parse_data(cls, call_data: str):
        args = {}
        for arg in call_data.split(cls.ARGS_SEP):
            key, value = arg.split(cls.ARG_SEP)
            if cls.VALUES_SEP in value:
                args[key] = value.split(cls.VALUES_SEP)
            else:
                args[key] = value

        call_type_name = args.pop(cls.CLASS_NAME)
        for key, value in cls.__dict__.items():
            if key == call_type_name:
                class_ = value
                return class_(**args)

    @classmethod
    def make_data(cls, call_type):
        args = {
            cls.CLASS_NAME: call_type.__class__.__name__,
        } | call_type.__dict__
        call_data = cls.ARGS_SEP.join(
            map(lambda key: f'{key}{cls.ARG_SEP}{args[key]}', args)
        )
        return call_data
