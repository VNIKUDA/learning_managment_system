from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.views import LoginView as DefaultLoginView, LogoutView as DefaultLogoutView
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_not_required
from account.forms import RegistrationForm, LoginForm
from django.shortcuts import redirect
from account.models import Profile

User = get_user_model()

# Create your views here.
@method_decorator(login_not_required, name="dispatch")
class LoginView(DefaultLoginView):
    form_class = LoginForm
    template_name = "account/login.html"


@method_decorator(login_not_required, name="dispatch")
class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = "account/register.html"
    success_url = reverse_lazy("account:login")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        if form.instance.role not in ["student", "teacher"]:
            raise ValidationError("When registrating new account, `role` field must be either a student or a teacher.")

        return super().form_valid(form)


class LogoutView(DefaultLogoutView):
    http_method_names = ["post"]


class ProfileView(DetailView):
    model = Profile
    context_object_name = "profile"
    template_name = "account/profile.html"

    def get_object(self):
        return Profile.objects.get(account=self.request.user)
    
class AccountUpdateView(DetailView):
    model = User
    context_object_name = "account"
    template_name = "account/account_update.html"

    def post(self, request: HttpRequest, *args, **kwargs):
        if self.request.FILES.get("picture"):
            picture = self.request.FILES.get("picture")
            self.request.user.profile.picture.save(picture.name, picture)

        self.request.user.username = self.request.POST.get("username")
        self.request.user.save()

        return redirect("account:profile")
    
    def get_object(self):
        return self.request.user