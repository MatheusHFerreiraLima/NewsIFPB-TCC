from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import CreateView, TemplateView
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import  HttpResponse
from django.urls import reverse_lazy
from imapclient import IMAPClient
from .models import EnviosEmails
from .models import Usuario
import feedparser
import datetime
import time
from django.utils.decorators import method_decorator


def obter_tempo_semana_passada():
    tempo_atual = time.time()
    uma_semana_atras = tempo_atual - (7 * 24 * 60 * 60)
    
    diferenca_horaria = datetime.timedelta(hours=3)  # Ajuste de 3 horas a mais
    tempo_ajustado = datetime.datetime.fromtimestamp(uma_semana_atras) + diferenca_horaria
    uma_semana_atras_ajustado = tempo_ajustado.timestamp()
    
    return uma_semana_atras_ajustado


def ler_noticias():
    # valor_controlador = 1683936034.0
    feed_url = 'https://www.ifpb.edu.br/ifpb/pedrasdefogo/noticias/todas-as-noticias-do-campus-pedras-de-fogo/RSS'
    rss = feedparser.parse(feed_url)
    noticias = rss.entries
    noticias_list = []
    for noticia in noticias:
        tempo_de_publicacao = time.mktime(noticia.published_parsed)
        if tempo_de_publicacao > obter_tempo_semana_passada():
            dados_noticia = {
                'url': noticia['link'],
                'titulo': noticia['title'],
                'img_href': None,
                'img_alt': noticia['title'].upper(),
                'descricao': noticia['summary']
            }
            noticias_list.append(dados_noticia)

    num_indices = len(noticias_list) 
    context = {'dados': noticias_list, 'num_indices': num_indices}
    
    return context



def descadastrar_email(view_func):
    def wrapper(request, *args, **kwargs):
        # Configurar a conexão IMAP
        server = IMAPClient('imap.gmail.com')
        server.login('naoresponda.newsifpb@gmail.com', 'dubzukogeeyyfyyr')

        pessoas_deletadas = []
        pessoas_nao_deletadas = []

        caixas = ['INBOX', '[Gmail]/Spam']

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

        request.descadastrar_email_context = context  # Armazene o contexto na requisição para acessá-lo posteriormente
        return view_func(request, *args, **kwargs)

    return wrapper

class UsuarioCreate(CreateView):
    model = Usuario
    fields = '__all__'

    def form_invalid(self, form):
        if 'email' in form.errors:
            form.add_error('email', 'Erro: esse email já está cadastrado. Insira um email válido.')
        return super().form_invalid(form)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        self.object = form.save()

        return redirect('polls:cadastro_realizado', email=email)

    @method_decorator(descadastrar_email)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
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
            resposta_bd = num_indices  # Cria a resposta para o banco de dados
            envio_emails = EnviosEmails.objects.create(quantidade_noticias=resposta_bd)  # Salva a resposta no banco de dados EnviosEmails

            envio_emails.destinatarios.set(Usuario.objects.all()) # Cria associações com os destinatários
            return HttpResponse('E-mails enviados com sucesso!')
        
        except Exception as e:
            return HttpResponse(f'Erro ao enviar e-mails: {str(e)}')

    else:
        num_indices = dados_das_noticias['num_indices']
        resposta_bd = num_indices  # Cria a resposta para o banco de dados
        envio_emails = EnviosEmails.objects.create(quantidade_noticias=resposta_bd)
        return HttpResponse('Não há conteúdo essa semana para ser enviado por e-mail. Portanto, o e-mail não foi enviado.')


class CadastroRealizadoView(TemplateView):
    template_name = 'polls/cadastro_realizado.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.kwargs['email']  # Certifique-se de usar 'self.kwargs['email']'
        return context

#TODO tamires, muda esse nome no reverse_lazy para configurar TUDO plmds e apaga essa var. Esse valor no reverse_lazy indica o caminho do urls.py que o html vai tomar ao receber o valor e processá-lo no banco. No entanto, para isso tem a lógica do que foi aprovado ou não, e isso eu deixo em tua mão dps que tu configurar o bendito usuario_form.html para fazer o crud e ajustar o css, html (que possivelmente tu vai fazer modificações) e o javascript. Boa sorte, hahaaha'

