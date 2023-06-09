import feedparser
from django.http import  HttpResponse
import time
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render



feed_url = 'https://www.ifpb.edu.br/ifpb/pedrasdefogo/noticias/todas-as-noticias-do-campus-pedras-de-fogo/RSS'

def teste(request):
    return render(request, 'polls/html/index.html')

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
    
# from django.core.files.base import ContentFile
# from .models import EnviosEmails
# def enviar_email():
#     usuarios = Usuario.objects.all()

#     dados_das_noticias = dados_email_view() 
#     if dados_das_noticias != {'dados': []}:

#         destinatarios = Usuario.objects.values_list('email', flat=True)
#         html_content = render_to_string("polls/email.html", dados_das_noticias)
#         text_content = strip_tags(html_content)



#         email = EmailMultiAlternatives('Newsletter IFPB teste', text_content, 'naoresponda.newsifpb@gmail.com', bbc=destinatarios)
#         email.attach_alternative(html_content, 'text/html')

#         try:    
#             email.send()
#             envio_emails = EnviosEmails.objects.create()
#             return HttpResponse('E-mails enviados com sucesso!')
        
#         except Exception as e:
#             return HttpResponse (f'Erro ao enviar e-mails: {str(e)}')

#     else:

#         return HttpResponse('Não há conteúdo para ser enviado para o e-mail. Portanto o e-mail não foi enviado')

