from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("popular/", views.popular, name="popular"),
    path("addquote/", views.addquote, name="addquote"),
    path("addquote/new_quote/", views.newquote, name="new_quote"),
    path("authenticate/", views.auth_view, name="authenticate"),
    path("authenticate/registration/", views.registration_view, name="registration"),
    path("authenticate/registration/reg/", views.registration, name="reg"),
    path("authenticate/auth/", views.auth, name="auth"),
    path("authenticate/auth/complete/", views.auth_complete, name="auth_complete"),
    path("authenticate/auth/complete/logout/", views.logout_view, name="logout"),
    path("<int:quote_id>/vote/", views.vote, name="vote"),
]