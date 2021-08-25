import datetime
from datetime import time

from django.contrib import auth, messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.forms.models import model_to_dict
from django.views.generic import ListView
import json
from .task import send_notifications

# Create your views here.
from django.conf import settings
from web.models import Notes, SharedNotes


class MypasswordChangeView(PasswordChangeView):
    template_name = 'user/password-change.html'
    success_url = reverse_lazy('passwordResetDoneView')


class MypasswordResetDoneView(PasswordResetDoneView):
    template_name = 'user/password-reset-done.html'


def login_frm(requests):
    return render(requests, 'login.html')


def do_login(request):
    if request.method == 'POST':
        username = request.POST['login-form-username']
        password = request.POST['login-form-password']

        user = authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            # messages.success(request, user.user_type)
            return redirect('technote_frm')

        else:

            messages.error(request, 'Invalid login credentials')
            return redirect('login_frm')
    messages.error(request, 'Something is Wrong, Please try again later')
    return redirect('login_frm')


def do_register(request):
    if request.method == 'POST':
        firstname = request.POST['register-form-firstname']
        lastname = request.POST['register-form-lastname']
        email = request.POST['register-form-email']
        username = request.POST['register-form-username']
        password = request.POST['register-form-password']
        repassword = request.POST['register-form-repassword']

        if password != repassword:
            messages.error(request, 'Password does not match')
            return redirect('login_frm')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username is already used')
            return redirect('login_frm')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered')
            return redirect('login_frm')

        try:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=firstname,
                                            last_name=lastname)
            user.save()
            messages.success(request, 'Successfully registered as ' + request.POST['register-form-username'])
            auth.login(request, user)
            # messages.success(request, user.user_type)
            return redirect('technote_frm')
        except Exception as e:
            messages.error(request, e)
            return redirect('login_frm')

    return None


@login_required(login_url='login_frm')
def technote_frm(request):
    # send_mail('subject', 'message', settings.EMAIL_HOST_USER, ['me.mahadi10@gmail.com'], fail_silently=True)
    # try:
    #
    #     # send_mail('subject', 'message', 'example@mail.com', ['itsmahadi@gmail.com'], fail_silently=True)
    #
    #     time_thresold = datetime.datetime.now() - datetime.timedelta(hours=2)
    #     # print(str(time_thresold))
    #     shared_obj = SharedNotes.objects.filter(seen=False)
    #
    #     # for i in shared_obj:
    #     #     print(i.note.title)
    #
    #     for i in shared_obj:
    #         subject = 'You have an Unread Notes from' + i.note.user.get_full_name()
    #         message = i.note.user.get_full_name() + ' has shared a note "' + i.note.title + '" with you'
    #         email_form = 'exmple@email.com'
    #         p = i.view_permit.first()
    #         email_obj = User.objects.get(username=p)
    #         # print(email_obj.email)
    #         recipient_list = [email_obj.email]
    #         print(message)
    #         send_mail(subject, message, email_form, recipient_list, fail_silently=True)
    #
    # except Exception as e:
    #     print(e)
    send_notifications.delay()
    my_note_obj = Notes.objects.filter(user=request.user)
    user_list = User.objects.all().exclude(username=request.user.username)

    # my_shared_obj = SharedNotes.objects.filter(note__user=request.user)
    # shared_with_me_obj = SharedNotes.objects.filter(view_permit__username=request.user.username)
    first_obj = my_note_obj.last()

    data = {
        'my_note': my_note_obj.order_by('title'),
        'first_obj': first_obj,
        'user_obj': user_list,

        # 'my_shared_note': my_shared_obj,
        # 'shared_with_me': shared_with_me_obj
    }
    return render(request, 'technote.html', data)


@login_required(login_url='login_frm')
def search_notes(request):
    if request.method == "POST":
        search_title = request.POST.get('search_data', None)
        if search_title:
            print(search_title)
            my_note_obj = Notes.objects.filter(user=request.user, title__icontains=search_title).order_by('modified_at')
            user_list = User.objects.all().exclude(username=request.user.username)
            first_obj = my_note_obj.last()
            filtered = True

            # for i in my_note_obj:
            #     print(i.title)
            # print(first_obj.title)
            #
            # for j in user_list:
            #     print(j.username)
            data = {
                'my_note': my_note_obj.order_by('title'),
                'first_obj': first_obj,
                'user_obj': user_list,
                'filter_ed': filtered,
                # 'my_shared_note': my_shared_obj,
                # 'shared_with_me': shared_with_me_obj
            }
            return render(request, 'technote.html', data)
        return redirect('technote_frm')


@login_required(login_url='login_frm')
def post_notes(request):
    if request.method != 'POST':
        return
    title = request.POST['title']
    content = request.POST['content']
    if request.POST['note_id'] != "null":
        note_id = int(request.POST['note_id'])
        print(note_id)
        if Notes.objects.filter(user=request.user, pk=note_id).exists():
            con_obj = Notes.objects.get(user=request.user, pk=note_id)
            con_obj.title = title
            con_obj.content = content.lstrip()
            con_obj.save()
            return redirect('technote_frm')
    else:
        obj = Notes(title=title, content=content.lstrip(), user=request.user)
        obj.save()
        return redirect('technote_frm')


@login_required(login_url='login_frm')
def get_notes(request, note_id):
    if Notes.objects.filter(user=request.user, pk=note_id).exists():
        obj = Notes.objects.get(user=request.user, pk=note_id)
        my_note_obj = Notes.objects.filter(user=request.user)
        user_list = User.objects.all().exclude(username=request.user.username)
        data = {
            'my_note': my_note_obj.order_by('title'),
            'first_obj': obj,
            'user_obj': user_list,
            # 'my_shared_note': my_shared_obj,
            # 'shared_with_me': shared_with_me_obj
        }
        return render(request, 'technote.html', data)


@login_required(login_url='login_frm')
def get_notes_shared_by_me(request, note_id):
    if SharedNotes.objects.filter(note__user=request.user).exists():
        oj = SharedNotes.objects.get(pk=note_id)
        obj = Notes.objects.get(user=request.user, pk=oj.note_id)

        my_shared_obj = SharedNotes.objects.filter(note__user=request.user)

        # shared_with_me_obj = SharedNotes.objects.filter(view_permit__username=request.user.username)

        data = {
            'my_note': my_shared_obj,
            'first_obj': obj,
            # 'my_shared_note': my_shared_obj,
            # 'shared_with_me': shared_with_me_obj
        }

        return render(request, 'technote_by_me.html', data)


@login_required(login_url='login_frm')
def get_notes_shared_with_me(request, note_id):
    if SharedNotes.objects.filter(view_permit__username=request.user.username).exists():
        obj = SharedNotes.objects.get(view_permit__username=request.user.username, note_id=note_id)
        if not obj.seen:
            obj.seen = True
            obj.save()
        shared_with_me_obj = SharedNotes.objects.filter(view_permit__username=request.user.username)

        # shared_with_me_obj = SharedNotes.objects.filter(view_permit__username=request.user.username)

        data = {
            'my_note': shared_with_me_obj,
            'first_obj': obj,
            # 'my_shared_note': my_shared_obj,
            # 'shared_with_me': shared_with_me_obj
        }

        return render(request, 'technote_with_me.html', data)


@login_required(login_url='login_frm')
def do_share_note(request, username, note_id):
    user_obj = User.objects.get(username=username)
    note_obj = Notes.objects.get(pk=note_id)

    try:
        obj = SharedNotes(note=note_obj)
        obj.save()
        obj.view_permit.add(user_obj)

        messages.success(request, "Shared " + note_obj.title + " with " + user_obj.get_full_name())

        # shared_obj = SharedNotes.objects.filter(seen=False, created_at__gte=time_thresold)
        subject = 'You have an Unread Notes from ' + request.user.get_full_name()
        message = request.user.get_full_name() + ' has shared a note  with you'
        email_form = request.user.email

        # print(email_obj.email)
        recipient_list = [user_obj.email]
        send_mail(subject, message, email_form, recipient_list)
        # try:
        #     send_mail(subject, email_form, 'admin@example.com', recipient_list, fail_silently=False)
        # except BadHeaderError:
        #     return HttpResponse('Invalid header found.')

        return redirect(technote_frm)
    except Exception as e:
        messages.error(request, e)
        return redirect(technote_frm)


@login_required(login_url='login_frm')
def delete_notes(request, note_id):
    obj = Notes.objects.get(user=request.user, pk=note_id)
    title = obj.title
    obj.delete()
    messages.info(request, title + " has been Deleted")
    return redirect('technote_frm')


@login_required(login_url='login_frm')
def technote_with_me_frm(request):
    # my_shared_obj = SharedNotes.objects.filter(note__user=request.user)
    shared_with_me_obj = SharedNotes.objects.filter(view_permit__username=request.user.username)
    first_obj = shared_with_me_obj.last()

    data = {
        'my_note': shared_with_me_obj,
        'first_obj': first_obj,
        # 'my_shared_note': my_shared_obj,
        # 'shared_with_me': shared_with_me_obj
    }
    return render(request, 'technote_with_me.html', data)


@login_required(login_url='login_frm')
def technote_by_me_frm(request):
    my_shared_obj = SharedNotes.objects.filter(note__user=request.user)
    # shared_with_me_obj = SharedNotes.objects.filter(view_permit__username=request.user.username)
    first_obj = my_shared_obj.last()

    data = {
        'my_note': my_shared_obj,
        'first_obj': first_obj,
        # 'my_shared_note': my_shared_obj,
        # 'shared_with_me': shared_with_me_obj
    }
    return render(request, 'technote_by_me.html', data)


@login_required(login_url='login_frm')
def account_frm(request):
    obj = User.objects.get(username=request.user.username)
    data = {
        'data': obj
    }
    return render(request, 'account.html', data)


@login_required(login_url='login_frm')
def account_update(request):
    if request.method == 'POST':
        obj = User.objects.get(username=request.user.username)
        firstname = request.POST['form-firstname']
        lastname = request.POST['form-lastname']
        email = request.POST['form-email']
        username = request.POST['form-username']

        if User.objects.filter(username=username).exists() and obj.username != username:
            messages.error(request, 'This username is already used')
            return redirect('account_frm')

        if User.objects.filter(email=email).exists() and obj.email != email:
            messages.error(request, 'This email is already registered')
            return redirect('account_frm')

        try:
            obj.first_name = firstname
            obj.last_name = lastname
            obj.username = username
            obj.email = email
            obj.save()
            messages.success(request, 'Successfully updated as ' + request.POST['form-username'])
            # messages.success(request, user.user_type)
            return redirect('technote_frm')
        except Exception as e:
            messages.error(request, e)
            return redirect('login_frm')

    return None


def log_out(request):
    # messages.success(request, 'you have logged out')
    logout(request)
    return HttpResponseRedirect("/")


from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "PASS/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="PASS/password_reset.html",
                  context={"password_reset_form": password_reset_form})
