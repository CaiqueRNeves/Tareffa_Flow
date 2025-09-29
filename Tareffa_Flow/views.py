from django.shortcuts import render
from .models import Tarefa


def Tareffa_Flow_list(request):
    Tarefas = Tarefa.objects.all()
    return render(request, "Tareffa_Flow/Tareffa_Flow_list.html", {"Tarefas": Tarefas})
