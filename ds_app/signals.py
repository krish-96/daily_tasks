from django.db.models.signals import pre_save, post_save
from .models import Ticket, TicketsLog

def save_ticket_user(sender, instance, **kwargs):
    print(f"{'='*100} \n save_ticket_user is callled and the title of the ticket is saved as  \n %s \n{'='*100} \n " % instance.title)
    ticket_log=TicketsLog.objects.create(created_by=instance.user.user)
    ticket_log.save()

post_save.connect(save_ticket_user, sender=Ticket)
