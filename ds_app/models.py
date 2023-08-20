from django.db import models
from django.contrib.auth.models import User

STATUS = (
    ('in_progress','In Progress'),
    ('done','Done'),
)

class Project(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"Project : {self.name}"

class Stream(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"Stream : {self.name}"


class UserProfile(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    stream = models.ForeignKey(Stream, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    password_changed = models.BooleanField(default=False)

    def __str__(self):
        return f"Name : {self.user.username} | Project : {self.project} | Stream : {self.stream}"


class Ticket(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, related_name='ticket_user')
    title = models.CharField(max_length=1000, blank=False, null=False)
    status = models.CharField(choices=STATUS,default='in_progress', max_length=12)


    def __str__(self):
        return f"Name : {self.user.user.username} | Status : {self.status} | Title : {self.title}"

class MailsTrack(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_mail_sent = models.BooleanField(default=False)
    mail_sent_date = models.DateField()

    def __str__(self):
        return f"Mail : {'Yes' if self.is_mail_sent == True else 'No'}"

class TicketsLog(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"Created by : {self.created_by.username}"
