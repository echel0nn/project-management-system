from django.contrib import admin
from .models import Team
from .models import UserProfile
from .models import Invite


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name','email','city','found_date']
    search_fields = ['name', 'social_name','city']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'team',]

class InviteAdmin(admin.ModelAdmin):
    list_display = ['inviter', 'invited',]
    search_fields = ['inviter', 'invited',]
    # list_filter = ['inviter', 'invited,']

# Register your models here.
admin.site.register(Team, TeamAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Invite, InviteAdmin)
