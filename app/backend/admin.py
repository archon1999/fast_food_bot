from django.contrib import admin

from backend.models import (BotUser,
                            Category,
                            Order,
                            ShopCard,
                            Product,
                            Template,
                            Purchase,
                            Info, 
                            Comment,
                            Review)


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

admin.site.register(ShopCard)


class CommentInline(admin.TabularInline):
    model = Comment

class InfoAdmins(admin.ModelAdmin):
    inlines = [
        CommentInline
    ]

admin.site.register(Info, InfoAdmins)