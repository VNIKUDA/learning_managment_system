from typing import Any, Iterable, MutableMapping
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinLengthValidator
from hashlib import shake_128

# Create your models here.

class Profile(models.Model):
    account = models.OneToOneField("Account", on_delete=models.CASCADE, related_name="profile")
    picture = models.ImageField(upload_to="profile_pictures/", blank=True)

    def __str__(self):
        return self.account.username

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

        Profile.objects.create(account=user)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
        )

        Profile.objects.create(account=user)

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
    REQUIRED_FIELDS = ["username"]

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        
        Profile.objects.get_or_create(account=self)


    @property
    def is_staff(self):
        return self.role in ["teacher", "admin"]
    
    @property
    def is_teacher(self):
        return self.role == "teacher"