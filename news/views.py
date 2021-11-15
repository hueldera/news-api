from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from news.models import Article, Author
from news.serializers import (
    ArticleAdminSerializer,
    AuthorAdminSerializer,
    ArticleSerializer,
    ArticleAnonymousSerializer,
)


class ArticleAdminModelViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleAdminSerializer
    permission_classes = [IsAdminUser]


class AuthorAdminModelViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorAdminSerializer
    permission_classes = [IsAdminUser]


class ArticleReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = Article.objects.select_related("author").all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        category = self.request.query_params.get("category")
        if category is not None:
            self.queryset = self.queryset.filter(category=category)

        return super().get_queryset()

    def get_serializer_class(self):
        self.serializer_class = (
            ArticleSerializer
            if self.request.user.is_authenticated
            else ArticleAnonymousSerializer
        )

        return super().get_serializer_class()
