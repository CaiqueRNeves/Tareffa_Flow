from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from .models import Tarefa


class TarefaListView(ListView):
    model = Tarefa
    template_name = "Tareffa_Flow/Tareffa_Flow_list.html"
    context_object_name = "Tarefas"


class TarefaCreateView(CreateView):
    model = Tarefa
    fields = ["title", "deadline", "descricao", "concluida"]
    success_url = reverse_lazy("tarefa_list")
