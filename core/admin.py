from django.contrib import admin
from .models import Subscribe, Faq, Contact

@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('email',)

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'created_at', 'updated_at')
    search_fields = ('question', 'answer')
    list_filter = ('created_at', 'updated_at')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'company', 'Message')
    search_fields = ('name', 'email', 'phone', 'company')
    list_filter = ('company',)
