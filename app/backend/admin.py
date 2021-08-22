from django.contrib import admin

from backend.models import (AboutShop, BotUser, Category, Order, Product,
                            Purchase, Review, ShopCard, Template)


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'contact', 'created']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_uz', 'parent']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title_uz', 'description_uz', 'price', 'category']


@admin.register(Review)
class ReviwAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'rating']


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['title', 'type']


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'count', 'created']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'created']


@admin.register(AboutShop)
class AboutShopAdmin(admin.ModelAdmin):
    list_display = ['title_uz', 'description_uz']
