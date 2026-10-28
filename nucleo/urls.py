from django.urls import path
from . import views

urlpatterns = [
    # Colaboradores
    path('', views.home, name='nucleo-inicial'),
    path('criar/', views.tela_criar, name='nucleo-criar'),
    path('salvar/', views.salvar, name='nucleo-salvar'),
    path('editar/<int:id>/', views.editar, name='nucleo-editar'),
    path('excluir/<int:id>/', views.excluir, name='nucleo-excluir'),

    # Equipamentos
    path(
        'equipamentos/',
        views.lista_equipamentos,
        name='equipamentos-lista'
    ),
    path(
        'equipamentos/criar/',
        views.tela_criar_equipamento,
        name='equipamento-criar'
    ),
    path(
        'equipamentos/salvar/',
        views.salvar_equipamento,
        name='equipamento-salvar'
    ),
    path(
        'equipamentos/editar/<int:id>/',
        views.editar_equipamento,
        name='equipamento-editar'
    ),
    path(
        'equipamentos/excluir/<int:id>/',
        views.excluir_equipamento,
        name='equipamento-excluir'
    ),
 # Empréstimos
path(
    'emprestimos/',
    views.lista_emprestimos,
    name='emprestimos-lista'
),
path(
    'emprestimos/criar/',
    views.tela_criar_emprestimo,
    name='emprestimo-criar'
),
path(
    'emprestimos/salvar/',
    views.salvar_emprestimo,
    name='emprestimo-salvar'
),
path(
    'emprestimos/editar/<int:id>/',
    views.editar_emprestimo,
    name='emprestimo-editar'
),
]