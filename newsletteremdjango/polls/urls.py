from django.urls import path
from . import views


# o nome de toda view é o (app_name:name), segundo Pedrinho, youtuber de 13 anos de idade
app_name = 'polls' 
urlpatterns = [
    path('oi/', views.oi, name="oi"),
    path('enviar/', views.enviar_email, name="enviar_email"),
    path ('teste/', views.teste, name="teste"),
    # path('processa_formulario/', views.processa_formulario, name="processa_formulario"),
    path('create/', views.UsuarioCreate.as_view(), name='create'),
    # path('deletar', views.deletar_usuarios.as_view(), name='deletar'),
    path('validacao/', views.validacao, name='validacao')

]
