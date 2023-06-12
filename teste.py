import imaplib
import email



def processar_emails():
    # Conectar-se ao servidor IMAP
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('naoresponda.newsifpb@gmail.com', 'dubzukogeeyyfyyr')

    # Selecionar a caixa de entrada
    mail.select('inbox')

    # Pesquisar e-mails não lidos
    status, response = mail.search(None, 'UNSEEN')

    return status

    # if status == 'OK':
    #     email_ids = response[0].split()
    #     for email_id in email_ids:
    #         # Obter o conteúdo do e-mail
    #         status, response = mail.fetch(email_id, '(RFC822)')
    #         if status == 'OK':
    #             raw_email = response[0][1]
    #             msg = email.message_from_bytes(raw_email)

    #             # Obter o endereço de e-mail do remetente
    #             remetente = msg['From']

    #             try:
    #                 # Descadastrar o usuário correspondente no banco de dados
    #                 a =3
    #                 return a
                    
    #             except ObjectDoesNotExist:
    #                 pass  # O usuário não existe, ou já foi descadastrado

    #             # Marcar o e-mail como lido
    #             mail.store(email_id, '+FLAGS', '\\Seen')

    # # Fechar a conexão com o servidor IMAP
    # mail.logout()

print(processar_emails())