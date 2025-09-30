from django.urls import path
from .views import (
    DashboardView,
    TarefaListView,
    TarefaDetailView,
    TarefaCreateView,
    TarefaUpdateView,
    TarefaDeleteView,
    TarefaCompleteView,
    TarefaClaimView,
    CommentCreateView,
)

urlpatterns = [
    path(
        "dashboard/", DashboardView.as_view(), name="dashboard"
    ),  # <- mudou de "" p/ "dashboard/"
    path("tarefas/", TarefaListView.as_view(), name="tarefa_list"),
    path("tarefas/create/", TarefaCreateView.as_view(), name="tarefa_create"),
    path("tarefas/<int:pk>/", TarefaDetailView.as_view(), name="tarefa_detail"),
    path("tarefas/<int:pk>/edit/", TarefaUpdateView.as_view(), name="tarefa_update"),
    path("tarefas/<int:pk>/delete/", TarefaDeleteView.as_view(), name="tarefa_delete"),
    path(
        "tarefas/<int:pk>/complete/",
        TarefaCompleteView.as_view(),
        name="tarefa_complete",
    ),
    path("tarefas/<int:pk>/claim/", TarefaClaimView.as_view(), name="tarefa_claim"),
    path(
        "tarefas/<int:pk>/comment/", CommentCreateView.as_view(), name="comment_create"
    ),
]
