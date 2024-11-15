from django.urls import path
from dictionary import views

urlpatterns = [
    path("get_definition_service/", views.get_definition_service, name="get_definition_service"),
    path("get_definition_llm/", views.get_definition_llm, name="get_definition_llm"),
    path("", views.home, name="home"),
]
