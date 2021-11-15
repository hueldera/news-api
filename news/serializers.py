from rest_framework.serializers import ModelSerializer, CharField
from .models import Article, Author


class AuthorAdminSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class ArticleAdminSerializer(ModelSerializer):
    firstParagraph = CharField(source="first_paragraph")

    class Meta:
        model = Article
        exclude = ("first_paragraph",)


class ArticleSerializer(ArticleAdminSerializer):
    author = AuthorAdminSerializer(many=False, read_only=True)


class ArticleAnonymousSerializer(ArticleSerializer):
    class Meta(ArticleSerializer.Meta):
        exclude = ("body",)
