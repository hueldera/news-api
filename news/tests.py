from factory.enums import CREATE_STRATEGY
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from news.models import Article, Author
from .factories import AuthorFactory, ArticleFactory
from users.factories import UserFactory
import json

User = get_user_model()


class ArticlesAdminTestCase(APITestCase):
    def setUp(self) -> None:
        self.client.force_authenticate(UserFactory(is_staff=True))
        return super().setUp()

    def test_create(self):
        article_data = {
            "author": AuthorFactory().id,
            "title": "Test Article",
            "category": "Category",
            "title": "Article title",
            "summary": "This is a summary of the article",
            "firstParagraph": "<p>This is the first paragraph of this article</p>",
            "body": "<div><p>Second paragraph</p><p>Third paragraph</p></div>",
        }
        response = self.client.post("/api/admin/articles/", article_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 1)

    def test_retrieve(self):
        article = ArticleFactory()
        response = self.client.get(f"/api/admin/articles/{article.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.data,
            {
                "id": str(article.id),
                "author": article.author.id,
                "category": article.category,
                "title": article.title,
                "summary": article.summary,
                "firstParagraph": article.first_paragraph,
                "body": article.body,
            },
        )

    def test_list(self):
        ArticleFactory.generate_batch(CREATE_STRATEGY, 3)
        response = self.client.get(f"/api/admin/articles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_update(self):
        article = ArticleFactory()
        response = self.client.put(
            f"/api/admin/articles/{article.id}/",
            {
                "id": str(article.id),
                "author": article.author.id,
                "category": "test",
                "title": "test",
                "summary": article.summary,
                "firstParagraph": article.first_paragraph,
                "body": article.body,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permission(self):
        author = AuthorFactory()
        client = APIClient()
        client.force_authenticate(UserFactory())
        response = client.get(f"/api/admin/authors/{author.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch(self):
        article = ArticleFactory()
        response = self.client.patch(
            f"/api/admin/articles/{article.id}/",
            {
                "body": "patched",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["body"], "patched")

    def test_delete(self):
        article = ArticleFactory()
        response = self.client.delete(f"/api/admin/articles/{article.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.count(), 0)


class AuthorsAdminTestCase(APITestCase):
    def setUp(self) -> None:
        self.client.force_authenticate(UserFactory(is_staff=True))
        return super().setUp()

    def test_create(self):
        author_data = {
            "name": "Test Author",
            "picture": "https://goole.com/test.png",
        }
        response = self.client.post("/api/admin/authors/", author_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 1)

    def test_retrieve(self):
        author = AuthorFactory()
        response = self.client.get(f"/api/admin/authors/{author.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.data,
            {
                "id": str(author.id),
                "name": author.name,
                "picture": author.picture,
            },
        )

    def test_permission(self):
        author = AuthorFactory()
        client = APIClient()
        client.force_authenticate(UserFactory())
        response = client.get(f"/api/admin/authors/{author.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list(self):
        AuthorFactory.generate_batch(CREATE_STRATEGY, 3)
        response = self.client.get(f"/api/admin/authors/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_update(self):
        author = AuthorFactory()
        response = self.client.put(
            f"/api/admin/authors/{author.id}/",
            {
                "id": str(author.id),
                "name": author.picture,
                "picture": "https://google.com/test2.png",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["picture"], "https://google.com/test2.png")

    def test_patch(self):
        author = AuthorFactory()
        response = self.client.patch(
            f"/api/admin/authors/{author.id}/",
            {
                "name": "patched",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "patched")

    def test_delete(self):
        author = AuthorFactory()
        response = self.client.delete(f"/api/admin/authors/{author.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)


class ArticlesTestCase(APITestCase):
    def setUp(self) -> None:
        self.client.force_authenticate(UserFactory())
        return super().setUp()

    def test_anonymous_list(self):
        client = APIClient()
        ArticleFactory.generate_batch(CREATE_STRATEGY, 5)
        response = client.get("/api/articles/")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 5)
        self.assertNotIn("body", response.data[0])

    def test_authenticated_list(self):
        ArticleFactory.generate_batch(CREATE_STRATEGY, 5)
        response = self.client.get("/api/articles/")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 5)
        self.assertIn("body", response.data[0])

    def test_anonymous_retrieve(self):
        client = APIClient()
        article = ArticleFactory()
        response = client.get(f"/api/articles/{article.id}/")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("body", response.data)
        self.assertIsInstance(response.data["author"], dict)

    def test_authenticated_retrieve(self):
        article = ArticleFactory()
        response = self.client.get(f"/api/articles/{article.id}/")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn("body", response.data)
        self.assertIsInstance(response.data["author"], dict)

    def test_category_filter(self):
        ArticleFactory.generate_batch(CREATE_STRATEGY, 5)
        ArticleFactory.generate_batch(CREATE_STRATEGY, 2, category="Category")
        response = self.client.get(f"/api/articles/?category=Category")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
