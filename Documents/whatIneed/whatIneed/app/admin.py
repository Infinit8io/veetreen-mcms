from django.contrib import admin

# Register your models here.
from app.models import Event, Inscription, Item, UserBringItem, ItemCategory

admin.site.register(Event)
admin.site.register(Inscription)
admin.site.register(Item)
admin.site.register(UserBringItem)
admin.site.register(ItemCategory)
