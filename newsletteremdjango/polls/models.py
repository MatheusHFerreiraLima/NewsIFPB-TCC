from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime 
import pytz

class Usuario(models.Model):
    email = models.EmailField(primary_key=True)

    def __str__(self):
        return self.email



class EnviosEmails(models.Model):
    resposta = models.CharField(max_length=255)
    data_envio = models.DateTimeField(auto_now_add=True)
    destinatarios = models.ManyToManyField(Usuario, blank=True, related_name="emails")

    class Meta:
        verbose_name_plural = "Envios de E-mails"

    def numero_email(self):
        emails_antes = EnviosEmails.objects.filter(data_envio__lt=self.data_envio)
        numero = emails_antes.count() + 1
        numero_formatado = str(numero).zfill(2)
        return numero_formatado

    def __str__(self):
        timezone = pytz.timezone('America/Sao_Paulo')
        data_local = self.data_envio.astimezone(timezone)
        data_formatada = data_local.strftime ("%d/%m/%Y")
        hora_formatada = data_local.strftime ("%H:%M:%S")

        return f"Envio do E-mail Nº {self.numero_email()} em {data_formatada} às {hora_formatada}"