from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as DefaultLoginView
from django.contrib.auth import get_user_model
from account.forms import RegistrationForm, LoginForm

User = get_user_model()

# Create your views here.
class LoginView(DefaultLoginView):
    form_class = LoginForm
    template_name = "account/login.html"


class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = "account/register.html"
    success_url = reverse_lazy("account:login")