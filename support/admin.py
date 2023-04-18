from django.contrib import admin
from .models import SupportTicket, Review
# Register your models here.

class CustomSupportTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'date')

class CustomReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'score', 'date')

admin.site.register(SupportTicket, CustomSupportTicketAdmin)
admin.site.register(Review, CustomReviewAdmin)