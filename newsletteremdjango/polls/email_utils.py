from django.core.management.base import BaseCommand
from django.conf import settings
from imapclient import IMAPClient
from polls.models import Usuario
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Configurar a conexão IMAP
        server = IMAPClient('imap.gmail.com')
        server.login('naoresponda.newsifpb@gmail.com', 'dubzukogeeyyfyyr')

        pessoas_deletadas = []
        pessoas_nao_deletadas = []

        # Buscar na caixa de entrada
        server.select_folder('INBOX')
        messages_inbox = server.search(['UNSEEN'])

        # Extrair remetentes e excluir usuários da caixa de entrada
        for msgid, data in server.fetch(messages_inbox, ['ENVELOPE']).items():
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

        server.set_flags(messages_inbox, [b'\\Seen'])
        # Buscar na caixa de spam
        server.select_folder('[Gmail]/Spam')
        messages_spam = server.search(['UNSEEN'])

        # Extrair remetentes e excluir usuários da caixa de spam
        for msgid, data in server.fetch(messages_spam, ['ENVELOPE']).items():
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


        # Marcar os e-mails como lidos na caixa de spam
        server.select_folder('[Gmail]/Spam')
        server.set_flags(messages_spam, [b'\\Seen'])

        # Fechar a conexão IMAP
        server.logout()

        context = {
            'pessoas_deletadas': pessoas_deletadas,
            'pessoas_nao_deletadas': pessoas_nao_deletadas
        }
        return context
