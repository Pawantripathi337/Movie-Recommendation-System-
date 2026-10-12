from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    # <str:...> (not <int:...>) so that a wrong id like /movie/abc/ shows a friendly message
    path("movie/<str:movie_id>/", views.movie_detail, name="movie_detail"),
    path("movie/<str:movie_id>/recommendations/", views.recommendations, name="recommendations"),
]
