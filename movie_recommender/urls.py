from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("movies.urls")),  # all website pages are defined in movies/urls.py
]
