from django.urls import path
from .views import get_resume, save_all_resume_embeddings, check_be_completion

urlpatterns = [
    path('get_resume/', get_resume, name='get_resume'),
    path('save_emmbed/', save_all_resume_embeddings, name='save_emmbed'),
    path('get_rows/', check_be_completion, name='get_rows'),
]
