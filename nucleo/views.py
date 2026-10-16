
from django.shortcuts import render, redirect, get_object_or_404
from nucleo.models import Colaborador


def home(req):
    busca = req.GET.get('busca', '').strip()
    colaboradores = Colaborador.objects.all().order_by('id')

    if busca:
        colaboradores = colaboradores.filter(nome__icontains=busca)

    return render(req, 'nucleo/index.html', {
        'colaboradores': colaboradores,
        'busca': busca,
    })


def tela_criar(req):
    return render(req, 'nucleo/forms/criar.html')


def salvar(req):
    if req.method == 'POST':
        nome = req.POST.get('nome', '').strip()
        telefone = req.POST.get('telefone', '').strip()

        if nome:
            Colaborador.objects.create(
                nome=nome,
                telefone=telefone
            )

    return redirect('nucleo-inicial')


def editar(req, id):
    colaborador = get_object_or_404(Colaborador, id=id)

    if req.method == 'POST':
        nome = req.POST.get('nome', '').strip()
        telefone = req.POST.get('telefone', '').strip()

        if nome:
            colaborador.nome = nome
            colaborador.telefone = telefone
            colaborador.save()
            return redirect('nucleo-inicial')

    return render(req, 'nucleo/forms/editar.html', {
        'colaborador': colaborador,
    })


def excluir(req, id):
    colaborador = get_object_or_404(Colaborador, id=id)

    if req.method == 'POST':
        colaborador.delete()

    return redirect('nucleo-inicial')
