from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import (
    ArticleAdminModelViewSet,
    AuthorAdminModelViewSet,
    ArticleReadOnlyModelViewSet,
)


router = SimpleRouter()
router.register("admin/articles", ArticleAdminModelViewSet)
router.register("admin/authors", AuthorAdminModelViewSet)
router.register("articles", ArticleReadOnlyModelViewSet)

urlpatterns = router.urls
