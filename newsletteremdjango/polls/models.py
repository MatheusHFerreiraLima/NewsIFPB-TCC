# from django.db import models
# from django.core.exceptions import ValidationError
# from django.utils import timezone

# class Usuario(models.Model):
#     email = models.EmailField(primary_key=True)

#     def clean(self):
#         existing_user = Usuario.objects.filter(email=self.email).exists()
#         if existing_user:
#             raise ValidationError('Este e-mail já está cadastrado.')


# class EnviosEmails(models.Model):
#     horario_envio = models.DateTimeField(default=timezone.now)
#     # Outros campos relevantes para o registro do envio

#     class Meta:
#         verbose_name_plural = "Envios de E-mails"

#     def __str__(self):
#         return f"Envio de E-mails em {self.horario_envio}"


