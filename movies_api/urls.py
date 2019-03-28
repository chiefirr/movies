from rest_framework.routers import DefaultRouter

from . import views

app_name = 'movies_api'

router = DefaultRouter()

router.register(r'movies', views.MovieViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = []
urlpatterns += router.urls
