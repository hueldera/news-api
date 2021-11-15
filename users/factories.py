from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from factory.faker import Faker


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = Faker("user_name")
    password = Faker("password")
