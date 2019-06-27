from django.contrib import admin
from .models import device, data
# Register your models here.


@admin.register(device)
class DeviceAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)


@admin.register(data)
class DataAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    search_fields = ('name',)
