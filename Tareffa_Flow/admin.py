from django.contrib import admin
from .models import Tarefa, Comment
from django.contrib import admin
from .models import Tarefa, Comment, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "avatar")


@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ("title", "criador", "concluida", "deadline", "finished_at")
    list_filter = ("concluida", "criador")
    search_fields = ("title", "descricao", "criador__username")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("tarefa", "autor", "created_at")
    search_fields = ("texto", "autor__username", "tarefa__title")
    list_filter = ("created_at",)
