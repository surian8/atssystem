from django.urls import path
from .views import get_resume, save_all_resume_embeddings

urlpatterns = [
    path('get_resume/', get_resume, name='get_resume'),
    path('save_emmbed/', save_all_resume_embeddings, name='save_emmbed'),
]
