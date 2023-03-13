from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post
from .forms import RegistrationForm, PostForm


# @login_required(login_url="/login")
# def homeView(request):
#     return render(request, "base/home.html", {"posts": Post.objects.all()})


class HomeView(LoginRequiredMixin, View):
    login_url = "/login"
    template_name = "main/home.html"

    def get(self, request):
        context = {
            "posts": Post.objects.all()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        post_id = request.POST.get("post-id")
        post = Post.objects.filter(id=post_id).first()
        if post and post.author == request.user:
            post.delete()
            return redirect("/home")
        context = {
            "posts": self.queryset
        }
        return render(request, self.template_name, context)


class CreatePost(LoginRequiredMixin, View):
    template_name = "main/create_post.html"
    login_url = "/login"

    def get(self, request, *args, **kwargs):
        form = PostForm()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home")
        else:
            form = PostForm()
        context = {
            "form": form
        }
        return render(request, self.template_name, context)


class UpdatePost(LoginRequiredMixin, View):
    login_url = "/login"
    template_name = "main/update_post.html"

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        form = PostForm(instance=post)
        context = {
            "form": form
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home")
        context = {
            "foms": form
        }
        return render(request, self.template_name, context)


class SignUp(View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        context = {"form": form}
        return render(request, "registration/sign_up.html", context)

    def post(self, request, *args, **kwargs):

        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/home")
        context = {
            "form": form
        }
        return render(request, "registration/sign_up.html", context)
