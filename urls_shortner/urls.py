from django.urls import include, path
from .views import ScrapeImageViewSet, ShortenURLAPIView, URLRedirectView
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('img', ScrapeImageViewSet, basename='scrape-images')


urlpatterns = [
    path('shorten/', ShortenURLAPIView.as_view(), name='url_shorten'),
    path('img/', ScrapeImageViewSet.as_view(), name='img'),
    path('<str:short_code>/', URLRedirectView.as_view(), name='url_redirect')
]
