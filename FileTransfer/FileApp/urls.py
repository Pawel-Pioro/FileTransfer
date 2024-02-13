from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path('upload/', views.upload_file, name='upload_file'),
    path('delete', views.delete_upload, name='delete_upload'),
]