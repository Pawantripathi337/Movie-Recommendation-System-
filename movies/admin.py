from django.contrib import admin

from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_year", "director", "vote_average", "popularity")
    search_fields = ("title", "director", "cast", "genres")
    list_filter = ("release_year",)
    ordering = ("-popularity",)
