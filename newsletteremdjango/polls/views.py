from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.views.generic import CreateView 
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.shortcuts import render
from .email_utils import Command
from django.http import  HttpResponse
from django.urls import reverse_lazy
from .models import EnviosEmails
from .models import Usuario
import feedparser
import time




feed_url = 'https://www.ifpb.edu.br/ifpb/pedrasdefogo/noticias/todas-as-noticias-do-campus-pedras-de-fogo/RSS'

def obter_tempo_inicial():
    return time.time()


def ler_noticias():
    rss = feedparser.parse(feed_url)
    noticias = rss.entries
    noticias_list = []
    for noticia in noticias:
        tempo_de_publicacao = time.mktime(noticia.published_parsed)
        if tempo_de_publicacao > 1683936034.0:
            dados_noticia = {
                'url': noticia['link'],
                'titulo': noticia['title'],
                'img_href': None,
                'img_alt': noticia['title'].upper(),
                'descricao': noticia['summary']
            }
            noticias_list.append(dados_noticia)

    tempo_inicial = obter_tempo_inicial()

    num_indices = len(noticias_list) 
    context = {'dados': noticias_list, 'num_indices': num_indices}
    
    return context
    
def enviar_newletter(request):
    dados_das_noticias = ler_noticias()
    if dados_das_noticias['dados'] != []:
        destinatarios = Usuario.objects.values_list('email', flat=True)
        html_content = render_to_string("polls/email.html", dados_das_noticias)
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



class UsuarioCreate (CreateView):
    model = Usuario
    fields ='__all__'
    success_url = reverse_lazy('polls:olhadescricao')

olhadescricao = 'tamires, muda esse nome no reverse_lazy para configurar TUDO plmds e apaga essa var. Esse valor no reverse_lazy indica o caminho do urls.py que o html vai tomar ao receber o valor e processá-lo no banco. No entanto, para isso tem a lógica do que foi aprovado ou não, e isso eu deixo em tua mão dps que tu configurar o bendito usuario_form.html para fazer o crud e ajustar o css, html (que possivelmente tu vai fazer modificações) e o javascript. Boa sorte, hahaaha'

def deletar_usuario(request):
    command = Command()
    context = command.handle()
    return render(request, 'polls/deletar_usuarios_emails_n_lidos.html', context)

        