from django.db import models
from django.db.models import F, Sum
from django.utils import timezone

from tinymce.models import HTMLField


def to_upper_underscore(text):
    return text.upper().replace(' ', '_')


class UserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            type=BotUser.Type.USER,
        )


class AdminManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            type=BotUser.Type.ADMIN,
        )


class CookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            type=BotUser.Type.COOK,
        )


class BotUser(models.Model):
    class Lang(models.TextChoices):
        UZ = 'uz'
        RU = 'ru'
        EN = 'en'

    class Type(models.TextChoices):
        USER = 'user'
        ADMIN = 'admin'
        COOK = 'cook'
        DRIVER = 'driver'

    objects = models.Manager()
    users = UserManager()
    admins = AdminManager()
    cooks = CookManager()

    type = models.CharField(
        max_length=10,
        choices=Type.choices,
        default=Type.USER
    )
    chat_id = models.IntegerField(unique=True)
    full_name = models.CharField(max_length=255, verbose_name="To'liq ismi")
    contact = models.CharField(max_length=50)
    balance = models.IntegerField(default=0)
    referal = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        related_name='referals',
        null=True,
        blank=True,
    )
    lang = models.CharField(
        max_length=10,
        choices=Lang.choices,
        default=Lang.UZ
    )
    bot_state = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    full_register = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = verbose_name + 'lar'

    def __str__(self):
        return self.full_name


class AdminPanel(models.Model):
    cook = models.CharField(max_length=50)
    driver = models.CharField(max_length=50)

class Category(models.Model):
    categories = models.Manager()
    name_uz = models.CharField(max_length=100, verbose_name='Nomi')
    name_ru = models.CharField(max_length=100, verbose_name='Название')
    name_en = models.CharField(max_length=100, verbose_name='Name')
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Ota kategoriya',
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_name(self, lang):
        return getattr(self, f'name_{lang}')

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = verbose_name + 'lar'

    def __str__(self):
        return self.name_uz


class Product(models.Model):
    products = models.Manager()
    title_uz = models.CharField(max_length=100, verbose_name='Nomi')
    title_ru = models.CharField(max_length=100, verbose_name='Название')
    title_en = models.CharField(max_length=100, verbose_name='Title')
    description_uz = models.TextField(verbose_name='Mahsulot haqida')
    description_ru = models.TextField(verbose_name='Описание')
    description_en = models.TextField(verbose_name='Description')
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        verbose_name='Kategoriya',
        related_name='products',
    )
    price = models.IntegerField(verbose_name='Narxi')
    image = models.ImageField(
        upload_to='backend/images/',
        default='backend/images/default.png',
        verbose_name='Rasm',
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_title(self, lang):
        return getattr(self, f'title_{lang}')

    def get_description(self, lang):
        return getattr(self, f'description_{lang}')

    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = verbose_name + 'lar'

    def __str__(self):
        return self.title_uz

class Prices(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title_uz = models.CharField(max_length=100, verbose_name='Nomi')
    title_ru = models.CharField(max_length=100, verbose_name='Название')
    title_en = models.CharField(max_length=100, verbose_name='Title')
    price = models.IntegerField()

    def get(self, lang):
        return getattr(self, f'title_{lang}')

    def __str__(self):
        return self.title_uz
    

class Purchase(models.Model):
    purchases = models.Manager()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def all_price(self):
        return self.price * self.count

    def __str__(self):
        return str(self.product)


class AboutShop(models.Model):
    title_uz = models.CharField(max_length=100, verbose_name='Nomi')
    title_ru = models.CharField(max_length=100, verbose_name='Название')
    title_en = models.CharField(max_length=100, verbose_name='Title')
    description_uz = HTMLField(verbose_name='haqida')
    description_ru = HTMLField(verbose_name='Описание')
    description_en = HTMLField(verbose_name='Description')
    contacts_and_location_uz = HTMLField(verbose_name='Bog`lanish va manzil')
    contacts_and_location_ru = HTMLField(verbose_name='Контакты и адрес')
    contacts_and_location_en = HTMLField(verbose_name='Contacts and location')

    image = models.ImageField(
        upload_to='backend/images/',
        verbose_name='Rasm'
    )

    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

    def get_title(self, lang):
        return getattr(self, f'title_{lang}')

    def get_description(self, lang):
        return getattr(self, f'description_{lang}')

    def get_contacts_and_location(self, lang):
        return getattr(self, f'contacts_and_location_{lang}')

    class Meta:
        verbose_name = 'Malumot'
        verbose_name_plural = verbose_name + 'lar'


class AboutBot(models.Model):
    title_uz = models.CharField(max_length=100, verbose_name='Nomi')
    title_ru = models.CharField(max_length=100, verbose_name='Название')
    title_en = models.CharField(max_length=100, verbose_name='Title')

    description_uz = HTMLField(verbose_name='haqida')
    description_ru = HTMLField(verbose_name='Описание')
    description_en = HTMLField(verbose_name='Description')

    def get_title(self, lang):
        return getattr(self, f'title_{lang}')

    def get_description(self, lang):
        return getattr(self, f'description_{lang}')


class Review(models.Model):
    reviews = models.Manager()
    user = models.OneToOneField(
        to=BotUser,
        on_delete=models.CASCADE,
        related_name='shop_review'
    )
    rating = models.IntegerField()
    description = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return str(self.rating)


class ShopCard(models.Model):
    shop_cards = models.Manager()
    user = models.OneToOneField(
        to=BotUser,
        on_delete=models.CASCADE,
        related_name='shop_card'
    )
    purchases = models.ManyToManyField(Purchase)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def price(self):
        price = self.purchases.aggregate(
            price_all=Sum(F('price')*F('count'))
        )['price_all']
        if not price:
            price = 0

        return price


class ActiveOrdersManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(
            status__in=[Order.Status.CANCELED, Order.Status.COMPLETED]
        )


class FinishedOrdersManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            status__in=[Order.Status.CANCELED, Order.Status.COMPLETED]
        )


class Order(models.Model):
    class PaymentType(models.TextChoices):
        CASH = 'Cash'
        PAYME = 'Payme'

    class DeliveryType(models.TextChoices):
        SELF_CALL = 'Self call'
        PAYMENT_DELIVERY = 'Payment delivery'

    class Status(models.TextChoices):
        RESERVED = 'Reserved'
        IN_QUEUE = 'In queue'
        PROCESSED = 'Processed'
        PREPARING = 'Preparing'
        COMPLETED = 'Completed'
        CANCELED = 'Canceled'

    orders = models.Manager()
    active = ActiveOrdersManager()
    finished = FinishedOrdersManager()
    user = models.ForeignKey(
        to=BotUser,
        on_delete=models.CASCADE,
        related_name='orders',
    )
    status = models.CharField(
        max_length=25,
        choices=Status.choices,
        default=Status.RESERVED,
    )
    delivery_type = models.CharField(
        max_length=20,
        choices=DeliveryType.choices,
    )
    payment_type = models.CharField(
        max_length=20,
        choices=PaymentType.choices
    )
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    purchases = models.ManyToManyField(Purchase)
    approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_trans_status(self, lang: str):
        status = to_upper_underscore(self.status)
        return Template.messages.get(title=status).get(lang)

    def get_trans_delivery_type(self, lang: str):
        delivery_type = to_upper_underscore(self.delivery_type)
        return Template.messages.get(title=delivery_type).get(lang)

    def __str__(self):
        return str(self.purchases)

    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = verbose_name + 'lar'


class UnfulfilledManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            date__lt=timezone.now(),
            done=False,
        )


class TaskManager(models.Model):
    class Type(models.TextChoices):
        OTHER = 'Other'

    SEP = '|'

    tasks = models.Manager()
    unfulfilled = UnfulfilledManager()
    type = models.CharField(max_length=30, choices=Type.choices)
    info = models.TextField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @classmethod
    def args_join(cls, *args):
        return cls.SEP.join(map(str, args))

    @property
    def argv(self):
        return self.info.split(TaskManager.SEP)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        if self.info:
            return f'{self.id}. {self.type}({self.info})'

        return f'{self.id}. {self.type}'


class KeyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='Key')


class MessageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='Message')


class SmileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='Smile')


class Template(models.Model):
    class Type(models.TextChoices):
        KEY = 'Key'
        MESSAGE = 'Message'
        SMILE = 'Smile'

    templates = models.Manager()
    keys = KeyManager()
    messages = MessageManager()
    smiles = SmileManager()

    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=Type.choices)
    body_uz = models.TextField()
    body_ru = models.TextField()
    body_en = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)

        keys = Template.keys.all()
        messages = Template.messages.all()
        smiles = Template.smiles.all()
        with open('backend/templates.py', 'w') as file:
            file.write('from .models import Template\n\n')
            file.write('\n')
            file.write('keys = Template.keys.all()\n')
            file.write('messages = Template.messages.all()\n')
            file.write('smiles = Template.smiles.all()\n\n')
            file.write('\n')
            file.write('class Keys():\n')
            for index, key in enumerate(keys):
                file.write(f'    {key.title} = keys[{index}]\n')

            file.write('\n\n')
            file.write('class Messages():\n')
            for index, message in enumerate(messages):
                file.write(f'    {message.title} = messages[{index}]\n')

            file.write('\n\n')
            file.write('class Smiles():\n')
            for index, smile in enumerate(smiles):
                file.write(f'    {smile.title} = smiles[{index}]\n')

        return result

    @property
    def text(self):
        return self.body_uz

    def get(self, lang):
        return getattr(self, f'body_{lang}')

    def getall(self):
        return (self.body_uz, self.body_ru, self.body_en)

    def format(self, **kwargs):
        return self.body_uz.format(**kwargs)

    def __format__(self, format_spec):
        return format(self.body_uz, format_spec)

    def __str__(self):
        return self.title
