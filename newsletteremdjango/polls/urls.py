from django.urls import path
from . import views


# o nome de toda view é o (app_name:name), segundo Pedrinho, youtuber de 13 anos de idade
app_name = 'polls' 
urlpatterns = [
    path('enviar/', views.enviar_newletter, name="enviar_newletter"),
    path('', views.UsuarioCreate.as_view(), name='create'),
    path('deletar_usuario/', views.deletar_usuario, name='deletar_usuario'),
]
