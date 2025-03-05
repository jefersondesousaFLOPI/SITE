# Testes automatizados do sistema
from django.test import TestCase
from django.urls import reverse
from .models import Usuario, Relatorio, Senha

class UsuarioTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(email='teste@exemplo.com', is_active=True)

    def test_usuario_list_view(self):
        response = self.client.get(reverse('gerenciar_usuarios'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'teste@exemplo.com')

    def test_usuario_edit_view(self):
        response = self.client.get(reverse('editar_usuario', args=[self.usuario.id]))
        self.assertEqual(response.status_code, 200)

    def test_usuario_delete_view(self):
        response = self.client.get(reverse('deletar_usuario', args=[self.usuario.id]))
        self.assertEqual(response.status_code, 302)  # Redireciona após a exclusão

class RelatorioTests(TestCase):
    def setUp(self):
        self.relatorio = Relatorio.objects.create(data='2023-01-01', total_atendimentos=10, total_receitas=1000)

    def test_relatorio_list_view(self):
        response = self.client.get(reverse('gerar_relatorio'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2023-01-01')

    def test_relatorio_data(self):
        self.assertEqual(self.relatorio.total_atendimentos, 10)
        self.assertEqual(self.relatorio.total_receitas, 1000)

class PainelTVTests(TestCase):
    def setUp(self):
        self.senha = Senha.objects.create(numero='001', tipo='Consulta')

    def test_painel_tv_view(self):
        response = self.client.get(reverse('painel_tv'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Senha: 001') 