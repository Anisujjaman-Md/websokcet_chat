from django.urls import path
from .views import ShortenURLAPIView, URLRedirectView

urlpatterns = [
    path('shorten/', ShortenURLAPIView.as_view(), name='url_shorten'),
    path('<str:short_code>/', URLRedirectView.as_view(), name='url_redirect'),
]
