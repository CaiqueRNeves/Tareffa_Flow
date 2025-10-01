from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Tarefa(models.Model):
    title = models.CharField("Título", max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)
    descricao = models.TextField(blank=True)
    concluida = models.BooleanField(default=False)
    # Usaremos 'criador' como RESPONSÁVEL atual da tarefa (claim)
    criador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tarefas",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-deadline"]

    def mark_has_completed(self):
        if not self.finished_at:
            self.finished_at = timezone.now()
            self.concluida = True
            self.save()

    def __str__(self):
        return self.title or ""


class Comment(models.Model):
    tarefa = models.ForeignKey(
        Tarefa, on_delete=models.CASCADE, related_name="comments"
    )
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comentário de {self.autor} em {self.tarefa}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.user.username


# Cria/atualiza o profile automaticamente


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    # garante que o profile exista mesmo se criado antes deste código
    if not hasattr(instance, "profile"):
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()
