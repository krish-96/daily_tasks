from django.contrib import admin
from .models import Ticket, Stream, UserProfile, Project, MailsTrack, TicketsLog


# Register your models here.


# class Profile(admin.ModelAdmin):
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    # list_display = ['created_time', 'updated_time', 'title', 'status', 'user']
    list_display = ['user', 'stream', 'project', 'password_changed']

    fieldsets = [
        ('User Information', {'fields': ('user',)}),
        ('Stream Information', {'fields': ('stream',)}),
        ('Project Information', {'fields': ('project',)}),
        ('Password Update Information', {'fields': ('password_changed',)}),
    ]


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    # list_display = ['created_time', 'updated_time', 'title', 'status', 'user']
    list_display = ['name', ]


class StreamAdmin(admin.ModelAdmin):
    model = Stream
    # list_display = ['created_time', 'updated_time', 'title', 'status', 'user']
    list_display = ['name', ]


class TicketAdmin(admin.ModelAdmin):
    model = Ticket
    list_display = ['created_time', 'updated_time', 'title', 'status', 'user']
    # list_display = ['title', 'status', 'user']

class TicketsLogAdmin(admin.ModelAdmin):
    model = TicketsLog
    list_display = ['created_time', 'updated_time', 'created_by']
    # list_display = ['title', 'status', 'user']


class MailsTrackAdmin(admin.ModelAdmin):
    model = MailsTrack
    list_display = ['mail_sent_date', 'is_mail_sent']

    fieldsets = [
        (
            "Mail sent On",
            {
                "fields": ["mail_sent_date"],
            },
        ),
        (
            "Mail Confirmation Status",
            {
                "classes": ["wide"],
                "fields": ["is_mail_sent"],
            },
        ),
    ]


admin.site.register(Ticket, TicketAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Stream, StreamAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(MailsTrack, MailsTrackAdmin)
admin.site.register(TicketsLog, TicketsLogAdmin)
