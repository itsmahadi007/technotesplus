from django.urls import path
from .views import *

urlpatterns = [
    path('', login_frm, name='login_frm'),
    path('do_login', do_login, name="do_login"),
    path('do_register', do_register, name="do_register"),
    path('technote/', technote_frm, name='technote_frm'),
    path('log_out', log_out, name='log_out'),
]
