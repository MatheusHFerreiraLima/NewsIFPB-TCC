import feedparser
from django.http import  HttpResponse
import time
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render
from django.core.files.base import ContentFile
from .models import EnviosEmails
from .models import Usuario



feed_url = 'https://www.ifpb.edu.br/ifpb/pedrasdefogo/noticias/todas-as-noticias-do-campus-pedras-de-fogo/RSS'


#testagem com forms.py:
#talvez essa próxima linha de import esteja errada também, não sei.
from newsletteremdjango.forms import UsuarioForm
def processa_formulario(request):
    data = {}
    data['form'] = UsuarioForm()
    return render(request, 'polls/html/index.html', data)

#testagem com redirecionamento de url (os dois estão incompletos, mas eu testaria o com forms.py):
# def processa_formulario(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         try:
#             usuario = Usuario(email=email)
#             usuario.full_clean()  # Validação do email
#             usuario.save()  # Salva no banco de dados
#             success_message = 'Seu e-mail foi cadastrado com sucesso!'
#             return render(request, 'polls/html/index.html', {'success_message': success_message})
#         except ValidationError as e:
#             error_message = str(e)
#             return render(request, 'polls/html/index.html', {'error_message': error_message})
#     return render(request, 'polls/html/index.html')

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
    dados_chamada = iterate_entries()
    dados_list = []
    dados_list.extend(dados_chamada)  # Adiciona os dados obtidos da função iterate_entries
    num_indices = len(dados_list)  # Conta o número de índices na lista dados_list
    context = {'dados': dados_list, 'num_indices': num_indices}  # Inclui o número de índices no contexto
    return context 

def enviar_email(request):
    dados_das_noticias = dados_email_view()
    if dados_das_noticias['dados'] != []:
        destinatarios = Usuario.objects.values_list('email', flat=True)
        html_content = render_to_string("polls/html/email.html", dados_das_noticias)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives('Newsletter IFPB teste', text_content, 'naoresponda.newsifpb@gmail.com', bcc=destinatarios)
        email.attach_alternative(html_content, 'text/html')

        try:
            email.send()
            num_indices = dados_das_noticias['num_indices']  # Obtém o número de índices da resposta do email
            resposta_bd = f"{num_indices} notícias foram geradas essa semana"  # Cria a resposta para o banco de dados
            envio_emails = EnviosEmails.objects.create(resposta=resposta_bd)  # Salva a resposta no banco de dados EnviosEmails

            envio_emails.destinatarios.set(Usuario.objects.all()) # Cria associações com os destinatários
            return HttpResponse('E-mails enviados com sucesso!')
        
        except Exception as e:
            return HttpResponse(f'Erro ao enviar e-mails: {str(e)}')

    else:
        num_indices = dados_das_noticias['num_indices']
        resposta_bd = f"{num_indices} notícias foram geradas essa semana"  # Cria a resposta para o banco de dados
        envio_emails = EnviosEmails.objects.create(resposta=resposta_bd)
        return HttpResponse('Não há conteúdo essa semana para ser enviado por e-mail. Portanto, o e-mail não foi enviado.')


