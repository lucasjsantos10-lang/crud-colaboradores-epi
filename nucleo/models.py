from django.db import models


class Colaborador(models.Model):
    nome = models.CharField(max_length=30, null=False, blank=False)
    telefone = models.CharField(max_length=30)

    def __str__(self):
        return self.nome


class Equipamento(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    descricao = models.TextField(blank=True)
    quantidade = models.PositiveIntegerField(default=0)
    ca = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.nome


class Emprestimo(models.Model):
    STATUS_CHOICES = [
        ('Emprestado', 'Emprestado'),
        ('Fornecido', 'Fornecido'),
        ('Devolvido', 'Devolvido'),
        ('Danificado', 'Danificado'),
        ('Perdido', 'Perdido'),
    ]

    colaborador = models.ForeignKey(
        Colaborador,
        on_delete=models.PROTECT,
        related_name='emprestimos'
    )

    equipamento = models.ForeignKey(
        Equipamento,
        on_delete=models.PROTECT,
        related_name='emprestimos'
    )

    data_entrega = models.DateTimeField()
    data_prevista_devolucao = models.DateTimeField()
    data_devolucao = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Emprestado'
    )

    observacao_devolucao = models.TextField(blank=True)

    def __str__(self):
        return f'{self.equipamento} - {self.colaborador}'