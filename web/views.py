import datetime
from datetime import time

from django.contrib import auth, messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.forms.models import model_to_dict
from django.views.generic import ListView
import json

# Create your views here.
from web.models import Notes, SharedNotes


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

            messages.error(request, 'Invalid login credentials 007')
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
    if request.method == 'POST':

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


def log_out(request):
    # messages.success(request, 'you have logged out')
    logout(request)
    return HttpResponseRedirect("/")
