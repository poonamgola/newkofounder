from django.contrib import admin
from .models import CustomUser, Review,Thread, ChatMessage


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'phone', 'nationality', 'gender', 'role', 'sector')
    search_fields = ('username', 'email', 'full_name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'reviewed_user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('reviewer__full_name', 'reviewed_user__full_name', 'content')
    raw_id_fields = ('reviewer', 'reviewed_user')

admin.site.register(ChatMessage)
class ChatMessage(admin.TabularInline):
    model = ChatMessage



class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread


admin.site.register(Thread, ThreadAdmin)