from django.contrib import admin
from .models import User, Progress, Player, Event

admin.site.register(User)
admin.site.register(Progress)
admin.site.register(Player)
admin.site.register(Event)
