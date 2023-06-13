from django.urls import path
from . import views


# o nome de toda view é o (app_name:name), segundo Pedrinho, youtuber de 13 anos de idade
app_name = 'polls' 
urlpatterns = [
    path('oi/', views.oi, name="oi"),
    path('enviar/', views.enviar_email, name="enviar_email"),
    path('create/', views.UsuarioCreate.as_view(), name='create'),
    path('validacao/', views.validacao, name='validacao'),
    path('deletar_usuario/', views.deletar_usuario, name='deletar_usuario'),


]
