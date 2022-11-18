from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import validate_email
from app.models.choices import ROLE_CHOICES
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from app.models.soft_delete import SoftDeleteModel
import environ

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, first_name, last_name, email, password,
                     **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        if not first_name:
            raise ValueError('Users require  first name')
        if not last_name:
            raise ValueError('Users require  first name')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, first_name, last_name, email, password=None,
                    **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        validate_email(email)
        return self._create_user(first_name, last_name, email, password,
                                 **extra_fields)

    def create_superuser(self, first_name, last_name, email, password,
                         **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(first_name, last_name, email, password,
                                 **extra_fields)


class User(AbstractUser, SoftDeleteModel):
    username = None

    first_name = models.CharField(
        'First Name',
        max_length=250
    )

    last_name = models.CharField(
        'Last Name',
        max_length=250
    )

    email = models.EmailField(
        'Email',
        max_length=100,
        unique=True
    )
    password = models.CharField(
        'Password',
        max_length=250
    )

    role = models.IntegerField(choices=ROLE_CHOICES, default=2)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email


@receiver(signal=post_save, sender=User)
def send_password(instance, **kwargs):
    password = BaseUserManager().make_random_password()
    user = User.objects.get(id=instance.id)
    if instance.role == 1:
        User.objects.filter(id=instance.id).update(
            is_staff=True, is_superuser=True)
    else:
        User.objects.filter(id=instance.id).update(
            is_staff=False, is_superuser=False)

    if len(user.password) == 0:
        user.set_password(password)
        user.save()
        send_mail(
            'Your Login Credentials',
            f"""Hello {user.first_name}, kindly find your login credentials
            below:
            email: {user.email}
            password: {password}
            """,
            env("EMAIL_HOST_USER"),
            [user.email, ],
            fail_silently=False,
        )