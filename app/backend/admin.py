from django.contrib import admin

from backend.models import (BotUser,
                            Category,
                            Order,
                            Product,
                            Template,
                            Purchase)


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'contact', 'created']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_uz', 'parent']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title_uz', 'description_uz', 'price', 'category']


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['title', 'type']


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'count', 'created']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'created']