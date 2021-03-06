from django.urls import path, include
from .views import *

urlpatterns = [
    path('', login_frm, name='login_frm'),
    path('do_login', do_login, name="do_login"),
    path('do_register', do_register, name="do_register"),
    path('technote/', technote_frm, name='technote_frm'),
    path('search_notes/', search_notes, name='search_notes'),
    path('technote_by_me/', technote_by_me_frm, name='technote_by_me_frm'),
    path('technote_with_me/', technote_with_me_frm, name='technote_with_me_frm'),
    path('post_note/', post_notes, name='post_notes'),
    path('get_notes/<int:note_id>', get_notes, name='get_notes'),
    path('get_notes_shared_by_me/<int:note_id>', get_notes_shared_by_me, name='get_notes_shared_by_me'),
    path('get_notes_shared_with_me/<int:note_id>', get_notes_shared_with_me, name='get_notes_shared_with_me'),
    path('delete_notes/<int:note_id>', delete_notes, name='delete_notes'),
    path('do_share_note/<username>/<int:note_id>', do_share_note, name='do_share_note'),
    path('account/', account_frm, name='account_frm'),
    path('account_update/', account_update, name='account_update'),
    path('change_password/', MypasswordChangeView.as_view(), name='passwordChangeView'),
    path('change_password/done', MypasswordResetDoneView.as_view(), name='passwordResetDoneView'),

    path("password_reset", password_reset_request, name="password_reset"),
    path('log_out', log_out, name='log_out'),
]
