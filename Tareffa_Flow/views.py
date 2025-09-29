from datetime import date
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect

from .models import Tarefa


class TarefaListView(ListView):
    model = Tarefa
    template_name = "Tareffa_Flow/Tareffa_Flow_list.html"
    context_object_name = "Tarefas"


class TarefaCreateView(CreateView):
    model = Tarefa
    fields = ["title", "deadline", "descricao", "concluida"]
    success_url = reverse_lazy("tarefa_list")


class TarefaUpdateView(UpdateView):
    model = Tarefa
    fields = ["title", "deadline", "descricao", "concluida"]
    success_url = reverse_lazy("tarefa_list")


class TarefaDeleteView(DeleteView):
    model = Tarefa
    success_url = reverse_lazy("tarefa_list")


class TarefaCompleteView(View):
    def get(self, request, pk):
        tarefa = get_object_or_404(Tarefa, pk=pk)
        tarefa.finished_at = date.today()
        tarefa.save()
        return redirect("tarefa_list")
