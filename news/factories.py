from factory.declarations import SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = "news.Author"

    name = Faker("name")
    picture = Faker("image_url")


class ArticleFactory(DjangoModelFactory):
    class Meta:
        model = "news.Article"

    author = SubFactory(AuthorFactory)
    category = Faker("color_name")
    title = Faker("name")
    summary = Faker("text")
    first_paragraph = Faker("text")
    body = Faker("text")
