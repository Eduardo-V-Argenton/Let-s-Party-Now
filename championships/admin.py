from django.contrib import admin
from .models import Championship

class CustomChampionshipAdmin(admin.ModelAdmin):
    list_display = ('id','championship_name', 'organizer')

admin.site.register(Championship, CustomChampionshipAdmin)