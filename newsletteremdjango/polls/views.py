from django.shortcuts import render
import feedparser
from django.http import  HttpResponse
import time
import datetime
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


feed_url = 'https://www.ifpb.edu.br/ifpb/pedrasdefogo/noticias/todas-as-noticias-do-campus-pedras-de-fogo/RSS'

def get_initial_time():
    return time.time()


def iterate_entries():
    rss = feedparser.parse(feed_url)
    entries = rss.entries
    data_list = []
    for entry in entries:
        published_time = time.mktime(entry.published_parsed)
        if published_time > 1683936034.0:
            data = {
                'url_noticia': entry['link'],
                'titulo_noticia': entry['title'],
                'img_href': None,
                'img_alt': entry['title'].upper(),
                'noticia_descricao': entry['summary']
            }
            data_list.append(data)
    initial_time = get_initial_time()
    return data_list
    



def dados_email_view():
    dados_chamada= iterate_entries()
    dados_list = [

    ]
    dados_list.extend(dados_chamada)  # Adiciona os dados obtidos da função iterate_entries
    context = {'dados': dados_list}
    return context
    


def enviar_email(request):
    html_content = render_to_string("polls/email.html", dados_email_view())
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives('Newsletter IFPB teste', text_content, 'matheus.lima.7@academico.ifpb.edu.br', ['matheus123henrique80academico@gmail.com', 'tamires.santana@academico.ifpb.edu.br'])

    email.attach_alternative(html_content, 'text/html')
    email.send()

    return HttpResponse(f'Olá, mundo')
# Create your views here.
