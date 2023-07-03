from django.urls import path
from . import views

# o nome de toda view é o (app_name:name), segundo Pedrinho, youtuber de 13 anos de idade
app_name = 'app' 
urlpatterns = [
    path('', views.UsuarioCreate.as_view(), name='create'),
    path('cadastro_realizado/<str:email>/', views.CadastroRealizadoView.as_view(), name='cadastro_realizado'),
    path('delete/<str:pk>/', views.UsuarioDelete.as_view(), name='delete'),
    path('cancel_success/<str:email>/', views.CancelSuccessView.as_view(), name='cancel_success'),
    path('enviar/', views.enviar_newsletter, name="enviar_newsletter"),
]
