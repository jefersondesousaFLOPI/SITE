# Sistema Web para Clínica

## Descrição
Este é um sistema web desenvolvido para gerenciar uma clínica, incluindo funcionalidades de agendamento, atendimento, financeiro e relatórios.

## Funcionalidades
- **Autenticação**: Tela de login e gerenciamento de usuários.
- **Menu Lateral**: Gerenciamento de acesso e opções do menu.
- **Sistema de Chamadas**: Painéis para emissão e atendimento de senhas.
- **Cadastros**: Cadastro de médicos, pacientes, convênios e exames.
- **Recepção**: Exibição do painel de chamadas e agendamento de consultas e exames.
- **Caixa**: Gerenciamento de pagamentos e fechamento do caixa.
- **Consultório Médico**: Listagem de pacientes com filtros.
- **Atendimento de Exames**: Listagem de pacientes agendados para exames.
- **Entrega de Exames**: Marcação de exames como entregues e exibição de telefone do paciente.
- **Relatórios**: Geração de relatórios em PDF e Excel.
- **Dashboard**: Exibição de totais de atendimentos, receitas, exames e consultas com gráficos interativos.

## Instruções de Instalação
1. Clone o repositório:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DO_DIRETORIO>
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute as migrações do banco de dados:
   ```bash
   python manage.py migrate
   ```
4. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```
5. Acesse o sistema em `http://127.0.0.1:8000/`

## Uso
- Acesse a tela de login com as credenciais do administrador:
  - E-mail: jefersonsoin@gmail.com
  - Senha: Npdjesus10/*
- Navegue pelas funcionalidades disponíveis no menu lateral.

## Testes
- Realize testes abrangentes conforme sugerido anteriormente para garantir que todas as funcionalidades estejam funcionando corretamente.

## Testes Automatizados
O sistema inclui testes automatizados para garantir a funcionalidade das principais áreas:

- **Gerenciar Usuários**: Testes para verificar a listagem, edição e exclusão de usuários.
- **Gerar Relatório**: Testes para validar a geração de relatórios e a exibição correta dos dados.
- **Painel de TV**: Testes para garantir que as senhas sejam exibidas corretamente no painel.

Para executar os testes, utilize o seguinte comando:
```
python manage.py test
```

## Tecnologias Utilizadas
- Django
- React
- PostgreSQL

## Como Executar
1. Instale as dependências do backend:
   ```
   pip install -r requirements.txt
   ```
2. Configure o banco de dados no arquivo settings.py.
3. Execute as migrações:
   ```
   python manage.py migrate
   ```
4. Inicie o servidor:
   ```
   python manage.py runserver
   ```
5. Para o frontend, navegue até a pasta frontend e execute:
   ```
   npm start
   ```

## Dashboard
- O dashboard exibe gráficos interativos que mostram informações relevantes sobre a clínica.
- **Gráfico de Barras**: Mostra os totais de atendimentos, receitas, exames e consultas.
- **Gráfico de Linha**: Mostra a evolução dos atendimentos ao longo do tempo, permitindo visualizar tendências e padrões. 