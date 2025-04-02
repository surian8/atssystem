from django.urls import path
from .views import  get_rows_by_prompt, get_user_by_embeddings

urlpatterns = [
    path('save_emmbed/', get_user_by_embeddings, name='save_emmbed'),
    path('get_rows/', get_rows_by_prompt, name='get_rows'),
]
