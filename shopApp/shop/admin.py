from django.contrib import admin

from .models import Category, Product, ProductComment


# Модель категории
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


# Модель товара
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}


class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['comment', 'created']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductComment, ProductCommentAdmin)
