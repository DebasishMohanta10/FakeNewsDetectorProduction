from django.shortcuts import render
from .clean_data import clean_text
# Create your views here.
import openai
import spacy
import time
from .fetch_data import fetch_data
from .response import generate_answer
from .fetch_urldata import fetch_url_data
import requests

from django.conf import settings
openai.api_key = settings.OPENAI_API_KEY
    
def current_affair(request):
    if request.method == 'GET':
        return render(request,"current.html")

    if request.method == 'POST':

        ques = request.POST['fakenews']

        # Load the pre-trained model
        nlp = spacy.load('en_core_web_sm')
        entities = []
        # Process the sentence using the loaded model
        doc = nlp(ques)

        # Iterate over the entities in the sentence
        for ent in doc.ents:
            # Print the entity text and its label
            entities.append(ent.text)

        articles = fetch_data(ques)
        if len(articles) == 0:
            if len(entities) != 0:
                articles = fetch_data(entities[0])
        formatted_response = generate_answer(ques,articles)

        sources = []
        for article in articles:
            sources.append({
                "url": article["url"],
                "headline": article["headline"],
                "date": article["date"],
                "publisher": article["publisher"]
            })

        context = {
            'formatted_response': clean_text(formatted_response),
            'prompt': ques,
            'sources': sources,
        }

        return render(request,"current.html",context)

def info(request):
    teams = Team.objects.all()
    context = {
        "teams": teams
    }
    return render(request,"info.html",context)

def grover(request):
    if request.method == 'GET':
        return render(request,"url.html")
    
    if request.method == 'POST':

        url = request.POST['news_url']

        data = fetch_url_data(url)
        articles = fetch_data(data)
        formatted_response = generate_answer(data,articles)

        context = {
            'formatted_response': formatted_response,
            'prompt': url,
        }
    return render(request,"url.html",context)



        

