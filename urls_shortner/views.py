from django.shortcuts import redirect
from rest_framework import generics
from .models import URL
from .serializers import URLSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from bs4 import BeautifulSoup
import requests
import json


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



class ScrapeImageViewSet(APIView):

    def get(self, request):
        url = "https://www.enosisbd.com/"  # Replace with your actual URL or take from request.data

        try:
            # Fetch the web page
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for HTTP errors
            html_content = response.text

            # Parse HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            print(soup)

            # Initialize response data structure
            response_data = {
                "total_error": 0,
                "errors": {}
            }

            # Check for <img> tags without alt attribute
            img_errors = self.check_img_tags(soup)
            if img_errors:
                response_data["errors"]["image"] = {
                    "error": "Alt tag missing",
                    "areas": img_errors
                }
                response_data["total_error"] += len(img_errors)

            # Check for <h1> tags without text content
            h1_errors = self.check_heading_tags(soup, 'h1')
            if h1_errors:
                response_data["errors"]["h1"] = h1_errors
                response_data["total_error"] += len(h1_errors)

            # Check for <h2> tags without text content
            h2_errors = self.check_heading_tags(soup, 'h2')
            if h2_errors:
                response_data["errors"]["h2"] = h2_errors
                response_data["total_error"] += len(h2_errors)

            h3_errors = self.check_heading_tags(soup, 'h3')
            if h3_errors:
                response_data["errors"]["h3"] = h3_errors
                response_data["total_error"] += len(h3_errors)

            # Return JSON response
            return Response(response_data)

        except requests.exceptions.RequestException as e:
            # Handle request errors
            error_response = {"error": str(e)}
            return Response(error_response, status=500)

    def check_img_tags(self, soup):
        img_tags = soup.find_all('img')
        img_errors = []

        for tag in img_tags:
            src = tag.get('src', 'N/A')
            alt = tag.get('alt')

            if not alt:
                line_no = tag.sourceline
                error_entry = {
                    "src": src,
                    "alt-text": alt,
                    "line_no": line_no
                }
                img_errors.append(error_entry)

        return img_errors

    def check_heading_tags(self, soup, tag_name):
        heading_tags = soup.find_all(tag_name)
        heading_errors = []

        for tag in heading_tags:
            text = tag.get_text(strip=True)

            if not text:
                line_no = tag.sourceline
                error_entry = {
                    "tag": tag_name,
                    "text": text,
                    "line_no": line_no
                }
                heading_errors.append(error_entry)

        return heading_errors