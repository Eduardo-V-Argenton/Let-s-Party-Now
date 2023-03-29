from django.contrib import admin
from .models import SupportTicket, Review
# Register your models here.

admin.site.register(SupportTicket)
admin.site.register(Review)