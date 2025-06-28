from django.contrib import admin
from .models import FootprintRecord, UserProfile

@admin.register(FootprintRecord)
class FootprintRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'total_footprint', 'created_at')
    list_filter = ('date', 'user')
    search_fields = ('user__username',)
    date_hierarchy = 'date'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'region', 'household_size')
    search_fields = ('user__username', 'region')
