from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="user-register"),
    path("login/", views.UserLoginView.as_view(), name="user-login"),
    path("logout/", views.UserLogoutView.as_view(), name="user-logout"),
    path("profile/", views.UserProfileView.as_view(), name="user-profile"),
    path("feeds/<str:username>/", views.UserFeedsView.as_view(), name="user-feeds"),
    path("reset/", views.UserPasswordResetView.as_view(), name="user-password-reset"),
    path(
        "reset/done/",
        views.UserPasswordResetDoneView.as_view(),
        name="user-password-reset-done",
    ),
    path(
        "confirm/<uidb64>/<token>/",
        views.UserPasswordResetConfirmView.as_view(),
        name="user-password-reset-confirm",
    ),
    path(
        "confirm/complete/",
        views.UserPasswordResetCompleteView.as_view(),
        name="user-password-reset-complete",
    ),
    path("follow/<int:user_id>/", views.UserFollowView.as_view(), name="user-follow"),
    path(
        "unfollow/<int:user_id>/",
        views.UserUnFollowView.as_view(),
        name="user-unfollow",
    ),
]
