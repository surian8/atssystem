from django.db import models

from pgvector.django import VectorField



class Resumes(models.Model):
    candidate_name = models.TextField()
    email = models.TextField(unique=True)
    phone = models.TextField(blank=True, null=True)
    # skills = models.TextField(blank=True, null=True)  # This field type is a guess.
    experience = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    resume_embedding = VectorField(dimensions=384)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'resumes'