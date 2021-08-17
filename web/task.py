from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.contrib.auth.models import User

from Tech_Note.celery import app
from .models import SharedNotes, Notes
import datetime
from django.core.mail import send_mail
from django.conf import settings


@app.task(name="send_notification")
def send_notification():
    try:
        # time_thresold = datetime.datetime.now() - datetime.timedelta(hours=2)
        # print(str(time_thresold))
        shared_obj = SharedNotes.objects.filter(seen=False)

        for i in shared_obj:
            subject = 'You have an Unread Notes from' + i.note.user.get_full_name()
            message = i.note.user.get_full_name() + ' has shared a note "' + i.note.title + '" with you'
            email_form = settings.EMAIL_HOST_USER
            p = i.view_permit.first()
            email_obj = User.objects.get(username=p)
            # print(email_obj.email)
            recipient_list = [email_obj.email]
            send_mail(subject, message, email_form, recipient_list, fail_silently=True)

    except Exception as e:
        print(e)


@shared_task(bind=True)
def send_notifications(self):
    try:
        # time_thresold = datetime.datetime.now() - datetime.timedelta(hours=2)
        # print(str(time_thresold))
        shared_obj = SharedNotes.objects.filter(seen=False)

        for i in shared_obj:
            subject = 'You have an Unread Notes from' + i.note.user.get_full_name()
            message = i.note.user.get_full_name() + ' has shared a note "' + i.note.title + '" with you'
            email_form = 'exmple@email.com'
            p = i.view_permit.first()
            email_obj = User.objects.get(username=p)
            # print(email_obj.email)
            recipient_list = [email_obj.email]
            #send_mail(subject, message, email_form, recipient_list, fail_silently=True)

    except Exception as e:
        print(e)
