# Generated by Django 4.2.2 on 2023-06-12 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_remove_usuario_envios_emails_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enviosemails',
            name='destinatarios',
            field=models.ManyToManyField(blank=True, related_name='emails', to='polls.usuario'),
        ),
    ]
