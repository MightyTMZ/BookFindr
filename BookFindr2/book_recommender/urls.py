from django.urls import path
from . import views

urlpatterns = [
    path('form/', views.chat_with_gpt),
    path('search/', views.search_book),
    path('temp/', views.search_book_view),
]