import requests
import json
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from .clean_data import clean_text

def deep_search(url):
    response = requests.get(url)

    if response.status_code == 200:
        content_type = response.headers.get('content-type')
        if 'application/json' in content_type:
            # Parse JSON data
            json_data = response.json()
            # Clean JSON data
            # ...
            print(json_data)
        elif 'text/html' in content_type:
            # Parse HTML data
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract text from HTML data
            text_content = ''
            for p in soup.find_all('h1'):
                text_content += clean_text(p.get_text())
            for p in soup.find_all('p'):
                text_content += clean_text(p.get_text())
            return text_content
        else:
            print('Unsupported content type: ' + content_type)
    else:
        print('Error fetching data: ' + str(response.status_code))