from django.db import models
from uuid import uuid4


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    picture = models.URLField()

    def __str__(self):
        return self.name


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=150)
    summary = models.TextField(max_length=320)
    first_paragraph = models.TextField()
    body = models.TextField()

    def __str__(self):
        return self.title
