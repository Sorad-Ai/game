from django.contrib import admin
from .models import tbl_proj

@admin.register(tbl_proj)
class MyTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'desc', 'like', 'view', 'date', 'keyword', 'link')
