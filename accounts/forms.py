from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Worker


class CustomUserCreationForm(UserCreationForm):

    role = forms.ChoiceField(
        choices=Worker.Role.choices, widget=forms.Select, label="Role"
    )

    class Meta:
        model = Worker
        fields = [
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "role",
        ]
