from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import CreateView 
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import  HttpResponse
from django.urls import reverse_lazy
from imapclient import IMAPClient
from .models import EnviosEmails
from .models import Usuario
import feedparser
import time


def obter_tempo_inicial():
    return time.time()


def ler_noticias():
    feed_url = 'https://www.ifpb.edu.br/ifpb/pedrasdefogo/noticias/todas-as-noticias-do-campus-pedras-de-fogo/RSS'
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
    success_url = reverse_lazy('polls:oi')

def oi(request):
    return HttpResponse('oi')

#TODO tamires, muda esse nome no reverse_lazy para configurar TUDO plmds e apaga essa var. Esse valor no reverse_lazy indica o caminho do urls.py que o html vai tomar ao receber o valor e processá-lo no banco. No entanto, para isso tem a lógica do que foi aprovado ou não, e isso eu deixo em tua mão dps que tu configurar o bendito usuario_form.html para fazer o crud e ajustar o css, html (que possivelmente tu vai fazer modificações) e o javascript. Boa sorte, hahaaha'

def descadastrar_email():
        # Configurar a conexão IMAP
        server = IMAPClient('imap.gmail.com')
        server.login('naoresponda.newsifpb@gmail.com', 'dubzukogeeyyfyyr')

        pessoas_deletadas = []
        pessoas_nao_deletadas = []
        
        #Lista de caixas:
        # Mailbox Name: INBOX
        # Mailbox Name: [Gmail]
        # Mailbox Name: [Gmail]/All Mail
        # Mailbox Name: [Gmail]/Drafts
        # Mailbox Name: [Gmail]/Important
        # Mailbox Name: [Gmail]/Sent Mail
        # Mailbox Name: [Gmail]/Spam
        # Mailbox Name: [Gmail]/Starred
        # Mailbox Name: [Gmail]/Trash
        caixas = ['INBOX','[Gmail]/Spam']
        
        for caixa in caixas:
        # Buscar na caixa de entrada
            server.select_folder(caixa)
            messagens = server.search(['UNSEEN'])

        # Extrair remetentes e excluir usuários da caixa de entrada
            for msgid, data in server.fetch(messagens, ['ENVELOPE']).items():
                envelope = data[b'ENVELOPE']

                sender_name = envelope.sender[0].name.decode('utf-8') if envelope.sender[0].name else ""
                sender_email = envelope.sender[0].mailbox.decode('utf-8') + "@" + envelope.sender[0].host.decode('utf-8')

            # Deletar o usuário com base no e-mail do remetente
                try:
                    usuario = Usuario.objects.get(email=sender_email)
                    usuario.delete()
                    pessoas_deletadas.append(sender_email)
                except Usuario.DoesNotExist:
                    pessoas_nao_deletadas.append(sender_email)

            server.set_flags(messagens, [b'\\Seen'])
        
        # Fechar a conexão IMAP
        server.logout()

        context = {
            'pessoas_deletadas': pessoas_deletadas,
            'pessoas_nao_deletadas': pessoas_nao_deletadas
        }
        return context

def deletar_usuario(request):
    context = descadastrar_email()

    return render(request, 'polls/deletar_usuarios_emails_n_lidos.html', context)
