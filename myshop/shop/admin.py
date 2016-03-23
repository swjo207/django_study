#-*- coding: utf-8 -*-
from django.contrib import admin
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    # name 필드를 입력하면 자동으로 slug에 채워짐
    prepopulated_fields = {'slug': ('name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','slug','price','stock','available','created','updated']
    list_filter = ['available','created','updated']
    list_editable = ['price','stock','available']
    # name 필드를 입력하면 자동으로 slug에 채워짐
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
