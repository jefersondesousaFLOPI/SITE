from django.db import models

class Usuario(models.Model):
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

class Permissao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pode_cadastrar = models.BooleanField(default=False)
    pode_atender = models.BooleanField(default=False)
    pode_visualizar = models.BooleanField(default=False)

class Medico(models.Model):
    nome = models.CharField(max_length=100)
    crm = models.CharField(max_length=20)

class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    convenio = models.CharField(max_length=100)

class Exame(models.Model):
    nome = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

class Senha(models.Model):
    tipo = models.CharField(max_length=20)
    numero = models.IntegerField()
    status = models.CharField(max_length=20, default='pendente')
    data_emissao = models.DateTimeField(auto_now_add=True)

class Chamada(models.Model):
    senha = models.ForeignKey(Senha, on_delete=models.CASCADE)
    setor = models.CharField(max_length=100)
    guiche = models.CharField(max_length=100)
    data_chamada = models.DateTimeField(auto_now_add=True)

class Pagamento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateTimeField(auto_now_add=True)

class Relatorio(models.Model):
    data = models.DateField()
    total_atendimentos = models.IntegerField()
    total_receitas = models.DecimalField(max_digits=10, decimal_places=2)

class HistoricoAtendimento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    data_atendimento = models.DateTimeField(auto_now_add=True)
    tipo_exame = models.CharField(max_length=100, null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True)

class ConteudoPainel(models.Model):
    tipo = models.CharField(max_length=20, choices=[('video', 'Vídeo'), ('imagem', 'Imagem')])
    url = models.URLField()
    ativo = models.BooleanField(default=True)

class Agendamento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    tipo = models.CharField(max_length=20, choices=[('consulta', 'Consulta'), ('exame', 'Exame')])
    status = models.CharField(max_length=20, default='agendado')

class PagamentoConsulta(models.Model):
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pendente')

class ConfiguracaoClinica(models.Model):
    nome = models.CharField(max_length=100)
    logo_url = models.URLField(null=True, blank=True)

class MenuLateral(models.Model):
    nome = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    ativo = models.BooleanField(default=True)

class Setor(models.Model):
    nome = models.CharField(max_length=100)
    contador = models.IntegerField(default=0) 