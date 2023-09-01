import requests
import json
from .clean_data import clean_text
from django.conf import settings

def fetch_data(query):

    # Define the API endpoint URL and query parameters
    url = "https://api.bing.microsoft.com/v7.0/news/search"
    params = {
        "q": query,
        "count": 10,
        "mkt": "en-IN",
    #     "freshness": "Day",
    #     "sortBy": "Date",
    #     "textDecorations": True,
        "textFormat": "HTML",
    }
    headers = {
        "Ocp-Apim-Subscription-Key": settings.KEY2
    }

    # Send a GET request to the API endpoint with the query parameters
    response = requests.get(url, params=params, headers=headers)

    # Check if the response status code is successful
    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    # Parse the response JSON data
    data = json.loads(response.text)

    # Check if the "value" key exists in the JSON data
    if "value" not in data:
        raise Exception(f"Invalid JSON response: {response.text}")
    # Extract the relevant news articles and metadata from the JSON data
    articles = []
    for item in data["value"]:
        article = {
            "headline": clean_text(item["name"]),
            "url": item["url"],
            "date": item["datePublished"],
            "publisher": item["provider"][0]["name"],
            "content": clean_text(item["description"])
        }
        articles.append(article)
    return articles


