from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from account.models import Relation

from home.models import Post
from .forms import UserRegistreationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


class UserRegisterView(View):
    template_name = "account/register.html"
    form_class = UserRegistreationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()

        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            User.objects.create_user(
                clean_data["username"], clean_data["email"], clean_data["password"]
            )
            messages.success(request, "You registred successfully.", "success")
            return redirect("home:home")
        context = {"form": form}
        return render(request, self.template_name, context)


class UserLoginView(View):
    template_name = "account/login.html"
    form_class = UserLoginForm

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get("next")
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()

        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            user = authenticate(
                request,
                username=clean_data["username"],
                password=clean_data["password"],
            )

            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in successfully.", "success")

                if self.next:
                    return redirect(self.next)
                
                return redirect("home:home")

        context = {"form": form}
        return render(request, self.template_name, context)


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logout successfully", "success")
        return redirect("home:home")


class UserProfileView(LoginRequiredMixin, View):
    template_name = "account/profile.html"

    def get(self, request):
        is_following = False
        user = get_object_or_404(User, id=request.user.id)
        posts = user.posts.all()
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        context = {"user": user, "posts": posts}

        return render(request, self.template_name, context)


class UserFeedsView(LoginRequiredMixin, View):
    template_name = "account/feeds.html"

    def get(self, request, *args, **kwargs):
        is_following = False
        user = get_object_or_404(User, username=kwargs["username"])
        posts = user.posts.all()
        relation = Relation.objects.filter(from_user=request.user, to_user=user)

        if relation.exists():
            is_following = True
        
        context = {"user": user, "posts": posts, "is_following": is_following}

        return render(request, self.template_name, context)


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = "account/password_reset_form.html"
    success_url = reverse_lazy("account:user-password-reset-done")
    email_template_name = "account/password_reset_email.html"


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "account/password_reset_done.html"


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "account/password_reset_confirm.html"
    success_url = reverse_lazy("account:user-password-reset-complete")


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "account/password_reset_complete.html"


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)

        if relation.exists():
            messages.error(request, "You are already following this user", "danger")
        else:
            Relation(from_user=request.user, to_user=user).save()
            messages.success(request, "You follow this user", "success")
        return redirect("account:user-feeds", user.username)


class UserUnFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)

        if relation.exists():
            relation.delete()
            messages.success(request, "You unfollowed this user", "success")

        else:
            messages.error(request, "You are not following this user", "danger")

        return redirect("account:user-feeds", user.username)
