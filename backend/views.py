from django.shortcuts import render, redirect
from .models import Medico, Paciente, Exame, Senha, Relatorio, Pagamento, HistoricoAtendimento, Usuario, ConteudoPainel, Agendamento, PagamentoConsulta, ConfiguracaoClinica, MenuLateral, Setor
from django.contrib.auth import authenticate, login
from django.db.models import Sum, Count
import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
import win32print
import win32ui
from django.utils import timezone
import pyttsx3

# Create your views here. 

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        user = authenticate(request, email=email, password=senha)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirecionar para a página inicial
    return render(request, 'login.html')


def register_medico(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        crm = request.POST['crm']
        Medico.objects.create(nome=nome, crm=crm)
        return redirect('home')
    return render(request, 'register_medico.html')


def register_paciente(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        data_nascimento = request.POST['data_nascimento']
        convenio = request.POST['convenio']
        Paciente.objects.create(nome=nome, data_nascimento=data_nascimento, convenio=convenio)
        return redirect('home')
    return render(request, 'register_paciente.html')


def register_exame(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        valor = request.POST['valor']
        Exame.objects.create(nome=nome, valor=valor)
        return redirect('home')
    return render(request, 'register_exame.html')


def emitir_senha(request):
    if request.method == 'POST':
        tipo = request.POST['tipo']
        numero = Senha.objects.count() + 1  # Incrementar o número da senha
        Senha.objects.create(tipo=tipo, numero=numero)
        return redirect('painel_chamadas')
    return render(request, 'emitir_senha.html')


def painel_chamadas(request):
    senhas = Senha.objects.all()
    return render(request, 'painel_chamadas.html', {'senhas': senhas})


def imprimir_senha(request, senha_id):
    senha = Senha.objects.get(id=senha_id)
    # Lógica para enviar a senha para a impressora
    printer_name = win32print.GetDefaultPrinter()
    hprinter = win32print.OpenPrinter(printer_name)
    try:
        hdc = win32ui.CreateDC('WINSPOOL', printer_name, None)
        hdc.StartDoc('Senha de Atendimento')
        hdc.StartPage()
        hdc.TextOut(100, 100, f'Senha: {senha.numero} - Tipo: {senha.tipo}')
        hdc.EndPage()
        hdc.EndDoc()
    finally:
        win32print.ClosePrinter(hprinter)
    senha.status = 'atendida'
    senha.save()
    return redirect('painel_chamadas')


def chamar_senha_por_voz(request, senha_id):
    senha = Senha.objects.get(id=senha_id)
    engine = pyttsx3.init()
    engine.say(f'Senha {senha.numero} do tipo {senha.tipo} chamada.')
    engine.runAndWait()
    return redirect('painel_chamadas')


def gerar_relatorio(request):
    total_atendimentos = Senha.objects.filter(status='atendida').count()
    total_receitas = Pagamento.objects.aggregate(Sum('valor'))['valor__sum'] or 0
    relatorio = Relatorio.objects.create(data=datetime.date.today(), total_atendimentos=total_atendimentos, total_receitas=total_receitas)
    relatorios = Relatorio.objects.all()
    return render(request, 'gerar_relatorio.html', {'relatorios': relatorios})


def registrar_pagamento(request):
    if request.method == 'POST':
        paciente_id = request.POST['paciente_id']
        valor = request.POST['valor']
        paciente = Paciente.objects.get(id=paciente_id)
        Pagamento.objects.create(paciente=paciente, valor=valor)
        return redirect('gerar_relatorio')
    pacientes = Paciente.objects.all()
    return render(request, 'registrar_pagamento.html', {'pacientes': pacientes})


def historico_atendimentos(request):
    atendimentos = HistoricoAtendimento.objects.all()
    return render(request, 'historico_atendimentos.html', {'atendimentos': atendimentos})


def gerar_relatorio_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, 'Relatório de Atendimentos')
    # Adicionar lógica para desenhar o relatório
    p.showPage()
    p.save()
    return response


def gerar_relatorio_excel(request):
    relatorios = Relatorio.objects.all()
    df = pd.DataFrame(list(relatorios.values()))
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="relatorio.xlsx"'
    df.to_excel(response, index=False)
    return response


def gerenciar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'gerenciar_usuarios.html', {'usuarios': usuarios})


def reiniciar_senhas_diariamente():
    if timezone.now().hour == 0:  # Verifica se é meia-noite
        Senha.objects.all().update(status='pendente')  # Reinicia todas as senhas para pendente 

def painel_tv(request):
    senhas = Senha.objects.filter(status='atendida')
    conteudos = ConteudoPainel.objects.filter(ativo=True)
    return render(request, 'painel_tv.html', {'senhas': senhas, 'conteudos': conteudos})


def atender_senha(request, senha_id):
    senha = Senha.objects.get(id=senha_id)
    # Lógica para atender a senha
    senha.status = 'atendida'
    senha.save()
    return redirect('painel_chamadas')


def cancelar_senha(request, senha_id):
    senha = Senha.objects.get(id=senha_id)
    # Lógica para cancelar a senha
    senha.status = 'cancelada'
    senha.save()
    return redirect('painel_chamadas')


def agendar_consulta(request):
    if request.method == 'POST':
        paciente_id = request.POST['paciente_id']
        medico_id = request.POST['medico_id']
        data_hora = request.POST['data_hora']
        Agendamento.objects.create(paciente_id=paciente_id, medico_id=medico_id, data_hora=data_hora, tipo='consulta')
        return redirect('historico_atendimentos')
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()
    return render(request, 'agendar_consulta.html', {'pacientes': pacientes, 'medicos': medicos})


def agendar_exame(request):
    if request.method == 'POST':
        paciente_id = request.POST['paciente_id']
        medico_id = request.POST['medico_id']
        data_hora = request.POST['data_hora']
        Agendamento.objects.create(paciente_id=paciente_id, medico_id=medico_id, data_hora=data_hora, tipo='exame')
        return redirect('historico_atendimentos')
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()
    return render(request, 'agendar_exame.html', {'pacientes': pacientes, 'medicos': medicos})


def caixa(request):
    pagamentos = PagamentoConsulta.objects.all()
    total = pagamentos.aggregate(Sum('valor'))['valor__sum'] or 0
    return render(request, 'caixa.html', {'pagamentos': pagamentos, 'total': total})


def confirmar_pagamento(request, pagamento_id):
    pagamento = PagamentoConsulta.objects.get(id=pagamento_id)
    pagamento.status = 'confirmado'
    pagamento.save()
    return redirect('caixa')


def gerenciar_configuracoes(request):
    configuracao = ConfiguracaoClinica.objects.first()
    if request.method == 'POST':
        configuracao.nome = request.POST['nome']
        configuracao.logo_url = request.POST['logo_url']
        configuracao.save()
        return redirect('gerenciar_configuracoes')
    return render(request, 'gerenciar_configuracoes.html', {'configuracao': configuracao})


def gerenciar_menu_lateral(request):
    menus = MenuLateral.objects.all()
    if request.method == 'POST':
        for menu in menus:
            menu.ativo = request.POST.get(f'menu_{menu.id}') == 'on'
            menu.save()
        return redirect('gerenciar_menu_lateral')
    return render(request, 'gerenciar_menu_lateral.html', {'menus': menus})


def gerenciar_setores(request):
    setores = Setor.objects.all()
    if request.method == 'POST':
        for setor in setores:
            setor.contador = request.POST.get(f'contador_{setor.id}', setor.contador)
            setor.save()
        return redirect('gerenciar_setores')
    return render(request, 'gerenciar_setores.html', {'setores': setores})


def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    if request.method == 'GET':
        nome = request.GET.get('nome')
        medico_id = request.GET.get('medico_id')
        if nome:
            pacientes = pacientes.filter(nome__icontains=nome)
        if medico_id:
            pacientes = pacientes.filter(medico_id=medico_id)
    medicos = Medico.objects.all()
    return render(request, 'listar_pacientes.html', {'pacientes': pacientes, 'medicos': medicos})


def listar_exames(request):
    exames = Agendamento.objects.filter(tipo='exame')
    if request.method == 'GET':
        nome = request.GET.get('nome')
        if nome:
            exames = exames.filter(paciente__nome__icontains=nome)
    return render(request, 'listar_exames.html', {'exames': exames})


def listar_exames_concluidos(request):
    exames_concluidos = Agendamento.objects.filter(tipo='exame', status='concluido')
    if request.method == 'GET':
        nome = request.GET.get('nome')
        if nome:
            exames_concluidos = exames_concluidos.filter(paciente__nome__icontains=nome)
    return render(request, 'listar_exames_concluidos.html', {'exames_concluidos': exames_concluidos})


def marcar_exame_entregue(request, exame_id):
    exame = Agendamento.objects.get(id=exame_id)
    exame.status = 'entregue'
    exame.save()
    return redirect('listar_exames_concluidos')


def dashboard(request):
    total_atendimentos = Senha.objects.filter(status='atendida').count()
    total_receitas = Pagamento.objects.aggregate(Sum('valor'))['valor__sum'] or 0
    total_exames = Agendamento.objects.filter(tipo='exame').count()
    total_consultas = Agendamento.objects.filter(tipo='consulta').count()

    # Obter dados de atendimentos ao longo do tempo
    atendimentos_por_dia = Senha.objects.filter(status='atendida').extra(select={'data': 'date(data_emissao)'}).values('data').annotate(total=Count('id')).order_by('data')
    datas = [atendimento['data'] for atendimento in atendimentos_por_dia]
    totais = [atendimento['total'] for atendimento in atendimentos_por_dia]

    return render(request, 'dashboard.html', {
        'total_atendimentos': total_atendimentos,
        'total_receitas': total_receitas,
        'total_exames': total_exames,
        'total_consultas': total_consultas,
        'datas': datas,
        'totais': totais
    }) 