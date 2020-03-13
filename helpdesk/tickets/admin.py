from django.contrib import admin
from .models import Ticket, Message
# Register your models here.

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'department', 'created_on','priority','status')
    list_filter = ('priority', 'status')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'message','published_by', 'published_at')
    list_filter = ('published_by',)

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Message, MessageAdmin)
