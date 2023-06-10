from django.contrib import admin

from .models import Usuario
from .models import EnviosEmails

admin.site.register(Usuario)
admin.site.register(EnviosEmails)

# Register your models here.
