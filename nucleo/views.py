
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from nucleo.models import Colaborador, Equipamento, Emprestimo
from django.utils import timezone
from django.db import transaction


# =========================
# COLABORADORES
# =========================

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

            messages.success(
                req,
                'Colaborador cadastrado com sucesso!'
            )

            return redirect('nucleo-inicial')

        messages.error(
            req,
            'Informe o nome do colaborador.'
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
            messages.success(req, 'Colaborador atualizado com sucesso!')
            return redirect('nucleo-inicial')

        messages.error(req, 'Informe o nome do colaborador.')

    return render(req, 'nucleo/forms/editar.html', {
        'colaborador': colaborador,
    })


def excluir(req, id):
    colaborador = get_object_or_404(Colaborador, id=id)

    if req.method == 'POST':
        colaborador.delete()
        messages.success(req, 'Colaborador excluído com sucesso!')

    return redirect('nucleo-inicial')


# =========================
# EQUIPAMENTOS
# =========================

def lista_equipamentos(req):
    equipamentos = Equipamento.objects.all().order_by('id')

    return render(req, 'nucleo/equipamentos.html', {
        'equipamentos': equipamentos,
    })


def tela_criar_equipamento(req):
    return render(req, 'nucleo/forms/criar_equipamento.html')


def salvar_equipamento(req):
    if req.method == 'POST':
        nome = req.POST.get('nome', '').strip()
        descricao = req.POST.get('descricao', '').strip()
        ca = req.POST.get('ca', '').strip()
        quantidade_texto = req.POST.get('quantidade', '').strip()

        try:
            quantidade = int(quantidade_texto)

            if not nome:
                messages.error(req, 'Informe o nome do equipamento.')

            elif quantidade < 0:
                messages.error(req, 'A quantidade não pode ser negativa.')

            else:
                Equipamento.objects.create(
                    nome=nome,
                    descricao=descricao,
                    ca=ca,
                    quantidade=quantidade,
                )
                messages.success(req, 'Equipamento cadastrado com sucesso!')

        except ValueError:
            messages.error(req, 'Informe uma quantidade válida.')

    return redirect('equipamento-criar')


def editar_equipamento(req, id):
    equipamento = get_object_or_404(Equipamento, id=id)

    if req.method == 'POST':
        nome = req.POST.get('nome', '').strip()
        descricao = req.POST.get('descricao', '').strip()
        ca = req.POST.get('ca', '').strip()
        quantidade_texto = req.POST.get('quantidade', '').strip()

        try:
            quantidade = int(quantidade_texto)

            if not nome:
                messages.error(req, 'Informe o nome do equipamento.')

            elif quantidade < 0:
                messages.error(req, 'A quantidade não pode ser negativa.')

            else:
                equipamento.nome = nome
                equipamento.descricao = descricao
                equipamento.ca = ca
                equipamento.quantidade = quantidade
                equipamento.save()

                messages.success(req, 'Equipamento atualizado com sucesso!')
                return redirect('equipamentos-lista')

        except ValueError:
            messages.error(req, 'Informe uma quantidade válida.')

    return render(req, 'nucleo/forms/editar_equipamento.html', {
        'equipamento': equipamento,
    })


def excluir_equipamento(req, id):
    equipamento = get_object_or_404(Equipamento, id=id)

    if req.method == 'POST':
        try:
            equipamento.delete()
            messages.success(req, 'Equipamento excluído com sucesso!')

        except Exception:
            messages.error(
                req,
                'Não foi possível excluir este equipamento. '
                'Verifique se ele está associado a algum empréstimo.'
            )

    return redirect('equipamentos-lista')


def lista_emprestimos(req):
    # Captura os filtros enviados pela tela
    colaborador_id = req.GET.get('colaborador', '').strip()
    equipamento_id = req.GET.get('equipamento', '').strip()
    status = req.GET.get('status', '').strip()

    # Inicia a consulta com todos os empréstimos
    emprestimos = Emprestimo.objects.select_related(
        'colaborador',
        'equipamento'
    ).all()

    # Aplica o filtro de colaborador
    if colaborador_id.isdigit():
        emprestimos = emprestimos.filter(
            colaborador_id=int(colaborador_id)
        )

    # Aplica o filtro de equipamento
    if equipamento_id.isdigit():
        emprestimos = emprestimos.filter(
            equipamento_id=int(equipamento_id)
        )

    # Aplica o filtro de status
    status_validos = [
        escolha[0] for escolha in Emprestimo.STATUS_CHOICES
    ]

    if status in status_validos:
        emprestimos = emprestimos.filter(status=status)

    # Organiza os registros do mais recente para o mais antigo
    emprestimos = emprestimos.order_by('-id')

    # Disponibiliza os dados e os filtros para o template
    return render(
        req,
        'nucleo/emprestimos.html',
        {
            'emprestimos': emprestimos,
            'colaboradores': Colaborador.objects.all().order_by('nome'),
            'equipamentos': Equipamento.objects.all().order_by('nome'),
            'status_choices': Emprestimo.STATUS_CHOICES,
            'filtro_colaborador': colaborador_id,
            'filtro_equipamento': equipamento_id,
            'filtro_status': status,
        }
    )

def tela_criar_emprestimo(req):
    colaboradores = Colaborador.objects.all().order_by('nome')
    equipamentos = Equipamento.objects.all().order_by('nome')

    return render(
        req,
        'nucleo/forms/criar_emprestimo.html',
        {
            'colaboradores': colaboradores,
            'equipamentos': equipamentos,
        }
    )

def salvar_emprestimo(req):
    if req.method == 'POST':
        colaborador_id = req.POST.get('colaborador')
        equipamento_id = req.POST.get('equipamento')
        data_entrega_texto = req.POST.get('data_entrega')
        data_prevista_texto = req.POST.get('data_prevista_devolucao')
        status = req.POST.get('status', 'Emprestado')

        status_validos = ['Emprestado', 'Fornecido']

        if status not in status_validos:
            messages.error(req, 'Selecione um status válido.')
            return redirect('emprestimo-criar')

        try:
            data_entrega = timezone.datetime.fromisoformat(
                data_entrega_texto
            )
            data_prevista = timezone.datetime.fromisoformat(
                data_prevista_texto
            )

            if timezone.is_naive(data_entrega):
                data_entrega = timezone.make_aware(data_entrega)

            if timezone.is_naive(data_prevista):
                data_prevista = timezone.make_aware(data_prevista)

            if data_prevista <= timezone.now():
                messages.error(
                    req,
                    'A previsão de devolução deve ser posterior '
                    'à data e hora atuais.'
                )
                return redirect('emprestimo-criar')

            if data_prevista <= data_entrega:
                messages.error(
                    req,
                    'A previsão de devolução deve ser posterior à entrega.'
                )
                return redirect('emprestimo-criar')

            with transaction.atomic():
                colaborador = get_object_or_404(
                    Colaborador,
                    id=colaborador_id
                )

                equipamento = get_object_or_404(
                    Equipamento.objects.select_for_update(),
                    id=equipamento_id
                )

                if equipamento.quantidade <= 0:
                    messages.error(
                        req,
                        'Este equipamento não possui unidades disponíveis '
                        'em estoque.'
                    )
                    return redirect('emprestimo-criar')

                equipamento.quantidade -= 1
                equipamento.save(update_fields=['quantidade'])

                Emprestimo.objects.create(
                    colaborador=colaborador,
                    equipamento=equipamento,
                    data_entrega=data_entrega,
                    data_prevista_devolucao=data_prevista,
                    status=status
                )

            messages.success(
                req,
                'Registro cadastrado com sucesso! O estoque foi atualizado.'
            )
            return redirect('emprestimos-lista')

        except (ValueError, TypeError):
            messages.error(
                req,
                'Confira as datas informadas e tente novamente.'
            )
            return redirect('emprestimo-criar')

    return redirect('emprestimo-criar')



def editar_emprestimo(req, id):
    emprestimo = get_object_or_404(Emprestimo, id=id)

    if req.method == 'POST':
        status = req.POST.get('status')
        data_devolucao_texto = req.POST.get(
            'data_devolucao', ''
        ).strip()
        observacao = req.POST.get(
            'observacao_devolucao', ''
        ).strip()

        status_validos = [
            'Emprestado',
            'Fornecido',
            'Devolvido',
            'Danificado',
            'Perdido',
        ]

        if status not in status_validos:
            messages.error(req, 'Selecione um status válido.')
            return redirect('emprestimo-editar', id=id)

        status_encerrados = ['Devolvido', 'Danificado', 'Perdido']

        if status in status_encerrados:
            if not data_devolucao_texto:
                messages.error(
                    req,
                    'Informe a data e hora da devolução, do dano ou da perda.'
                )
                return redirect('emprestimo-editar', id=id)

            try:
                data_devolucao = timezone.datetime.fromisoformat(
                    data_devolucao_texto
                )

                if timezone.is_naive(data_devolucao):
                    data_devolucao = timezone.make_aware(data_devolucao)

            except ValueError:
                messages.error(req, 'Informe uma data e hora válida.')
                return redirect('emprestimo-editar', id=id)
        else:
            data_devolucao = None
            observacao = ''

        with transaction.atomic():
            equipamento = get_object_or_404(
                Equipamento.objects.select_for_update(),
                id=emprestimo.equipamento_id
            )

            status_anterior = emprestimo.status

            estava_em_aberto = status_anterior in [
                'Emprestado',
                'Fornecido',
            ]

            ficara_em_aberto = status in [
                'Emprestado',
                'Fornecido',
            ]

            # Se estava aberto e será encerrado, devolve ao estoque.
            if estava_em_aberto and not ficara_em_aberto:
                equipamento.quantidade += 1
                equipamento.save(update_fields=['quantidade'])

            # Se estava encerrado e voltará a ficar aberto, retira do estoque.
            elif not estava_em_aberto and ficara_em_aberto:
                if equipamento.quantidade <= 0:
                    messages.error(
                        req,
                        'Não há unidades disponíveis para reabrir '
                        'este empréstimo.'
                    )
                    return redirect('emprestimo-editar', id=id)

                equipamento.quantidade -= 1
                equipamento.save(update_fields=['quantidade'])

            emprestimo.status = status
            emprestimo.data_devolucao = data_devolucao
            emprestimo.observacao_devolucao = observacao
            emprestimo.save()

        messages.success(req, 'Empréstimo atualizado com sucesso!')
        return redirect('emprestimos-lista')

    return render(
        req,
        'nucleo/forms/editar_emprestimo.html',
        {'emprestimo': emprestimo}
    )
