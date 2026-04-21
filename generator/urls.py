"""App URL routing."""
from django.urls import path

from . import views


app_name = "generator"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("type-to-image/", views.type_to_image_view, name="type_to_image"),
    path("script-to-image/", views.script_to_image_view, name="script_to_image"),
    path("history/", views.history_view, name="history"),
    path("history/<int:pk>/", views.history_detail_view, name="history_detail"),
]
