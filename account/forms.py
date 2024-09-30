from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationForm(UserCreationForm):
    usable_password = None

    role = forms.ChoiceField(choices=(("student", "Студент"), ("teacher", "Вчитель")))

    class Meta():
        model = User
        fields = ["email", "username", "password1", "password2", "role"]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    def save(self, commit: bool = ...) -> Any:
        return super().save(commit)


class LoginForm(AuthenticationForm):
    def __init__(self, request: Any = ..., *args: Any, **kwargs: Any) -> None:
        super().__init__(request, *args, **kwargs)


        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"