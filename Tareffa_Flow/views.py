from datetime import date
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)

from .models import Tarefa, Comment, UserProfile
from .forms import (
    ProfileForm,
    UserProfileForm,  # <-- IMPORT ESSENCIAL
    TarefaForm,
    CommentForm,
    SignUpForm,
)
from django.core.cache import cache
from .services.news import fetch_news


# ---------- Auth ----------
class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class AuthLoginView(LoginView):
    template_name = "registration/login.html"


class AuthLogoutView(LogoutView):
    pass


from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Home pública com slider, cards e seção sobre (notícias dinâmicas)."""

    template_name = "Tareffa_Flow/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        news = cache.get("home_news")
        if news is None:
            news = fetch_news(limit_total=6)
            cache.set("home_news", news, 60 * 10)  # 10 min
        ctx["news"] = news
        return ctx


# ---------- Dashboard ----------
class DashboardView(LoginRequiredMixin, ListView):
    template_name = "Tareffa_Flow/dashboard.html"
    context_object_name = "minhas_tarefas"

    def get_queryset(self):
        # Tarefas atribuídas ao usuário logado (usamos 'criador' como responsável)
        return Tarefa.objects.filter(criador=self.request.user).order_by(
            "concluida", "deadline"
        )


# ---------- Permissões ----------
class SomenteResponsavelMixin(UserPassesTestMixin):
    def test_func(self):
        tarefa = self.get_object()
        return self.request.user.is_staff or tarefa.criador == self.request.user


# ---------- Tarefas ----------
class TarefaListView(LoginRequiredMixin, ListView):
    model = Tarefa
    template_name = "Tareffa_Flow/Tareffa_Flow_list.html"
    context_object_name = "Tarefas"
    # Lista geral (pode filtrar aqui se quiser só as suas)


class TarefaDetailView(LoginRequiredMixin, DetailView):
    model = Tarefa
    template_name = "Tareffa_Flow/tarefa_detail.html"
    context_object_name = "tarefa"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comment_form"] = CommentForm()
        return ctx


class TarefaCreateView(LoginRequiredMixin, CreateView):
    model = Tarefa
    form_class = TarefaForm
    template_name = "Tareffa_Flow/tarefa_form.html"
    success_url = reverse_lazy("tarefa_list")

    def form_valid(self, form):
        # por padrão, quem cria vira responsável
        if not form.instance.criador:
            form.instance.criador = self.request.user
        return super().form_valid(form)


class TarefaUpdateView(LoginRequiredMixin, SomenteResponsavelMixin, UpdateView):
    model = Tarefa
    form_class = TarefaForm
    template_name = "Tareffa_Flow/tarefa_form.html"
    success_url = reverse_lazy("tarefa_list")


class TarefaDeleteView(LoginRequiredMixin, SomenteResponsavelMixin, DeleteView):
    model = Tarefa
    template_name = "Tareffa_Flow/tarefa_confirm_delete.html"
    success_url = reverse_lazy("tarefa_list")


class TarefaCompleteView(LoginRequiredMixin, SomenteResponsavelMixin, View):
    def get(self, request, pk):
        tarefa = get_object_or_404(Tarefa, pk=pk)
        tarefa.finished_at = date.today()
        tarefa.concluida = True
        tarefa.save()
        return redirect("tarefa_list")


class TarefaClaimView(LoginRequiredMixin, View):
    """Tomar para si: usuário vira o responsável (criador)."""

    def post(self, request, pk):
        tarefa = get_object_or_404(Tarefa, pk=pk)
        tarefa.criador = request.user
        tarefa.save()
        return redirect("tarefa_detail", pk=tarefa.pk)


# ---------- Comentários ----------
class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        tarefa = get_object_or_404(Tarefa, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                tarefa=tarefa, autor=request.user, texto=form.cleaned_data["texto"]
            )
        return redirect("tarefa_detail", pk=tarefa.pk)


# ---------- Perfil ----------
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "Tareffa_Flow/profile.html"


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "Tareffa_Flow/profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user

    def _ensure_profile(self):
        # garante que o user tenha profile antes de usar
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        profile = self._ensure_profile()
        if self.request.method == "POST":
            ctx["profile_form"] = UserProfileForm(
                self.request.POST, self.request.FILES, instance=profile
            )
        else:
            ctx["profile_form"] = UserProfileForm(instance=profile)
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        profile = self._ensure_profile()

        user_form = self.get_form()
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Perfil atualizado com sucesso.")
            return self.form_valid(user_form)

        messages.error(request, "Corrija os erros abaixo e tente novamente.")
        return self.form_invalid(user_form)
