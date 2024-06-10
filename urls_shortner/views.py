from django.shortcuts import redirect
from rest_framework import generics
from .models import URL
from .serializers import URLSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class ShortenURLAPIView(APIView):
    def post(self, request, format=None):
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid():
            original_url = serializer.validated_data['original_url']
            url_object = URL.objects.create(original_url=original_url)
            # Retrieve the generated short URL
            short_url = request.build_absolute_uri('/') + url_object.short_code
            return Response({'short_url': short_url}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class URLRedirectView(generics.RetrieveAPIView):
    queryset = URL.objects.all()
    serializer_class = URLSerializer
    lookup_field = 'short_code'

    @method_decorator(cache_page(1200, key_prefix="my_cache_prefix"))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Redirect to the original URL
        return redirect(instance.original_url)
