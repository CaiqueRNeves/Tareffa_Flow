from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tarefa, Comment
from .models import UserProfile
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ["title", "deadline", "descricao", "concluida"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["texto"]
        widgets = {
            "texto": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Escreva um comentário..."}
            )
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["avatar"]
        widgets = {"avatar": forms.FileInput(attrs={"class": "form-control"})}

    def clean_avatar(self):
        file = self.cleaned_data.get("avatar")
        if not file:
            return file
        max_mb = 5
        if file.size > max_mb * 1024 * 1024:
            raise forms.ValidationError(f"A imagem deve ter no máximo {max_mb}MB.")
        valid_mimes = {"image/jpeg", "image/png", "image/webp"}
        if hasattr(file, "content_type") and file.content_type not in valid_mimes:
            raise forms.ValidationError("Use uma imagem JPG, PNG ou WEBP.")
        return file
