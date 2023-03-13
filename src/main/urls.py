from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("home/", views.HomeView.as_view(), name="home"),
    path("sign-up/", views.SignUp.as_view(), name="sign-up"),
    path("create-post/", views.CreatePost.as_view(), name="create-post"),
    path("update-post/<int:id>", views.UpdatePost.as_view(), name="update-post")
]
