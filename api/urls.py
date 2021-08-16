from django.urls import path, include
from .views import *

urlpatterns = [
    path("", apioverview, name="api-over-view "),
    path("notes/", Note_gp.as_view()),
    path("shared_by_me/", Shared_by_me.as_view()),
    path("shared_with_me/", Shared_with_me.as_view()),
    path("admiral/", include("django_expiring_token.urls")),  # <-- for custome token expireing url

]
