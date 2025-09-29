from django.db import models
from django.conf import settings


class Tarefa(models.Model):
    title = models.CharField(
        verbose_name="Título", max_length=200, null=False, blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    deadline = models.DateTimeField(null=False, blank=False)
    finished_at = models.DateTimeField(null=True, blank=True)
    descricao = models.TextField(blank=True)
    concluida = models.BooleanField(default=False)
    criador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tarefas",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-deadline"]

    def __str__(self):
        return self.title
