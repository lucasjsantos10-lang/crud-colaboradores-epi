
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='nucleo-inicial'),
    path('criar', views.tela_criar, name='nucleo-criar'),
    path('salvar', views.salvar, name='nucleo-salvar'),
    path('editar/<int:id>', views.editar, name='nucleo-editar'),
    path('excluir/<int:id>', views.excluir, name='nucleo-excluir'),
]
