from django.shortcuts import render
from django.http import JsonResponse
from neo4j import GraphDatabase
import os
from django.http import JsonResponse
from .models import Resumes
from django.db.models.signals import post_save
from django.dispatch import receiver
from pgvector.django import L2Distance
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text):
    return model.encode(text).tolist()





def save_all_resume_embeddings(request):
    resumes = Resumes.objects.all()  # Fetch all resumes
    for resume in resumes:
        text = f"{resume.candidate_name} {resume.email} {resume.phone} {resume.experience} {resume.education}"
        embedding = generate_embedding(text)
        resume.resume_embedding = embedding  # Store embedding as a vector
        resume.save()  # Save changes for each resume

    return JsonResponse({"message": f"Embeddings updated for {len(resumes)} resumes."})
    


# @receiver(post_save, sender=Resumes)
# def generate_embedding_on_save(sender, instance, **kwargs):
#     if not instance.embedding:  # Only generate if embedding is missing
#         instance.embedding = generate_embedding(f"{instance.name} {instance.summary} {instance.skills} {instance.experience} {instance.education}")
#         instance.save()

    
    
def get_resume(request):
    query_text = "Backend Developer"
        
    query_embedding = generate_embedding(query_text)
    resumes = Resumes.objects.alias(
                distance=L2Distance("resume_embedding", query_embedding)
            ).order_by("distance")[:5]
    results = [
                {"id": r.id, "name": r.candidate_name, "email": r.email, "phone": r.phone, "experience": r.experience, "education": r.education}
                for r in resumes
            ]
    return JsonResponse({"results": results}, status=200)

    
    


