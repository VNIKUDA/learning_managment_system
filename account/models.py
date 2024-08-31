from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinLengthValidator
from hashlib import shake_128

# Create your models here.

class Profile(models.Model):
    account = models.OneToOneField("Account", on_delete=models.CASCADE, related_name="profile")
    picture = models.ImageField(upload_to="profile_pictures/")


class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.role = "admin"
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    ROLE_CHOICES = (
        ("student", "Студент"),
        ("teacher", "Вчитель"),
        ("admin", "Адмін")
    )

    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    username = models.CharField(max_length=255, validators=[MinLengthValidator(5, 'Поле "Username" не повинно бути менше 5 символів')])
    role = models.CharField(default="student", choices=ROLE_CHOICES, max_length=30)
    
    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


