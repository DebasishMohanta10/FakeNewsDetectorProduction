import openai
from django.conf import settings
openai.api_key = settings.OPENAI_API_KEY
from .deep_search import deep_search


def generate_answer(question, articles):
    context = ''
    for article in articles:
        context += article['headline'] + '\n\n'
        context += article['content'] + '\n\n'
        context += "Date Which the News was published on:" + article['date'][:10] + '\n\n'
        # data = deep_search(article['url'])
        # if data:
        #     context += data
    if len(articles) > 0:
        data1 = deep_search(articles[0]['url'])
        if data1:
            context += data1
    
    context = context[0:4096]
    prompt = f"{context}\nQ: {question}.Do all Content analysis and fact checking to specify Real or Fake with supportive answer.Use Reliable sources word insted of context.Don't give sources.\nA:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    answer = response.choices[0].text.strip()
    return answer