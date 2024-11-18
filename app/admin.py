# keywords/admin.py
from django.contrib import admin
from .models import Category, Keyword,ScrapedResult
admin.site.register(Category)
admin.site.register(Keyword)
admin.site.register(ScrapedResult)
