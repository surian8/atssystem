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

def get_rows(request):
    resumes = Resumes.objects.all()
    results = [
                {"id": r.id, "name": r.candidate_name, "email": r.email, "phone": r.phone, "experience": r.experience, "education": r.education}
                for r in resumes
            ]
    return JsonResponse({"results": results}, status=200)




from django.http import JsonResponse
import json
from langchain_community.chat_models import ChatOllama
from langchain.schema import SystemMessage, HumanMessage
from langchain.output_parsers import PydanticOutputParser


from pydantic import BaseModel

class BECheckResponse(BaseModel):
    has_be: bool  # AI should return True or False


# Load Ollama LLM (Change model if needed)
llm = ChatOllama(model="gemma3:1b")

# Pydantic parser for structured AI response
parser = PydanticOutputParser(pydantic_object=BECheckResponse)

def get_user_embeddings(user_ids):
    """Retrieve education text for a list of user IDs."""
    resumes = Resumes.objects.filter(id__in=user_ids).values("id", "education","experience")
    return {
            r["id"]: {
                "education": r["education"],
                "experience": r["experience"],
            }
            for r in resumes
        }
# ...existing code...

def check_be_completion(request):
    """Check if users have completed a BE degree using Pydantic + Ollama."""
    try:
        user_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        prompt_temp = "Does this person have a BE degree? Respond only with JSON."

        if not user_ids:
            return JsonResponse({"error": "User IDs required"}, status=400)

        user_data = get_user_embeddings(user_ids)
        results = {}
        print(parser.get_format_instructions())
        
        
       

        for user_id, user_details in user_data.items():
            education = user_details["education"]
            experience = user_details["experience"]
            messages = [
                SystemMessage(content="You are an AI that checks if a person has completed a Bachelor of Engineering (BE). Respond in JSON format."),
                HumanMessage(content=f"""
                    Here is the candidate's information:
                    - Education: {education}
                    - Experience: {experience}
                    {prompt_temp}
                    Output should be in Boolean format. it should be True or False only two options  other format is not accepted.
                """)
            ]

            response = llm.invoke(messages).content.strip()
            print(response)

            # Validate and handle unexpected responses
            try:
                # parsed_response = response  # Validate AI output
                results[user_id] = response  # Store the boolean result
            except Exception as e:
                # Log the error and return a default value
                results[user_id] = None
                print(f"Error parsing response for user {user_id}: {e}")

        return JsonResponse({"results": results}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    


