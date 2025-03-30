from django.shortcuts import render
from django.http import JsonResponse
from neo4j import GraphDatabase
import os
from django.http import JsonResponse
from django.db.models.signals import post_save
from django.dispatch import receiver
from pgvector.django import L2Distance
from sentence_transformers import SentenceTransformer
from django.db import models
from pgvector.django import VectorField

class Resumes(models.Model):
    candidate_name = models.TextField()
    email = models.TextField(unique=True)
    phone = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)  # This field type is a guess.
    experience = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    resume_embedding = VectorField(dimensions=768)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'resumes'

model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text):
    return model.encode(text).tolist()




def save_all_resume_embeddings(request):
    resumes = Resumes.objects.all()  # Fetch all resumes
    for resume in resumes:
        text = f"{resume.candidate_name} {resume.email} {resume.phone} {resume.skills} {resume.experience} {resume.education}"
        embedding = generate_embedding(text)
        resume.embedding = embedding  # Store embedding as a vector
        resume.save()  # Save changes for each resume

    return f"Embeddings updated for {len(resumes)} resumes."
    
