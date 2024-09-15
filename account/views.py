from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib.auth.views import LoginView as DefaultLoginView, LogoutView as DefaultLogoutView
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_not_required
from account.forms import RegistrationForm, LoginForm
from account.models import Profile

User = get_user_model()

# Create your views here.
@method_decorator(login_not_required, name="dispatch")
class LoginView(DefaultLoginView):
    form_class = LoginForm
    template_name = "account/login.html"


@method_decorator(login_not_required, name="dispatch")
class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = "account/register.html"
    success_url = reverse_lazy("account:login")


class LogoutView(DefaultLogoutView):
    http_method_names = ["post"]


class ProfileView(DetailView):
    model = Profile
    context_object_name = "profile"
    template_name = "account/account.html"

    def get_object(self):
        return Profile.objects.get(account=self.request.user)