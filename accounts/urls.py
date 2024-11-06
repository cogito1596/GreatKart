from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("acticate/<uidb64>/<token>", views.activate, name="activate"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("forgot-password/", views.forgot_password, name="forgot-password"),
    path("resetPassword/", views.reset_password, name="resetPassword"),
    path(
        "reset_password_validate/<uidb64>/<token>",
        views.reset_password_validate,
        name="resetpassword_validate",
    ),
]
