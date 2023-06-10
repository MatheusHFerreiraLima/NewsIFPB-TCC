from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime 
import pytz

class Usuario(models.Model):
    email = models.EmailField(primary_key=True)

    def clean(self):
        existing_user = Usuario.objects.filter(email=self.email).exists()
        if existing_user:
            raise ValidationError('Este e-mail já está cadastrado.')
    def __str__(self):
        return self.email

    envios_emails = models.ManyToManyField('EnviosEmails', blank=True)


class EnviosEmails(models.Model):
    resposta = models.CharField(max_length=255)
    data_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Envios de E-mails"

    def __str__(self):
        timezone = pytz.timezone('America/Sao_Paulo')
        data_local = self.data_envio.astimezone(timezone)
        data_formatada = data_local.strftime ("%d/%m/%Y %H:%M:%S")
        return f"Envio do E-mail em {data_formatada}"