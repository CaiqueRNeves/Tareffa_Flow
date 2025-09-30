from django.contrib import admin
from django.urls import path, include
from Tareffa_Flow.views import (
    AuthLoginView,
    AuthLogoutView,
    SignUpView,
    ProfileView,
    ProfileEditView,
    HomeView,
)
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    # Home pública
    path("", HomeView.as_view(), name="home"),
    # Admin
    path("admin/", admin.site.urls),
    # Autenticação
    path("accounts/login/", AuthLoginView.as_view(), name="login"),
    path("accounts/logout/", AuthLogoutView.as_view(), name="logout"),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    # Perfil
    path("accounts/profile/", ProfileView.as_view(), name="profile"),
    path("accounts/profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
    # Alterar senha
    path(
        "accounts/password/change/",
        PasswordChangeView.as_view(
            template_name="registration/password_change_form.html",
            success_url="/accounts/password/change/done/",
        ),
        name="password_change",
    ),
    path(
        "accounts/password/change/done/",
        PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name="password_change_done",
    ),
    # App principal
    path("", include("Tareffa_Flow.urls")),
]

# mídia em dev
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
