from bs4 import BeautifulSoup

def clean_text(text):
    soup = BeautifulSoup(text, "html.parser")
    plain_text = soup.get_text()
    return plain_text