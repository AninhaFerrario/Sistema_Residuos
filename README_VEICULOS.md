# Sistema de Gestão de Veículos - Projeto Resíduo

## Descrição
Sistema completo de CRUD para gestão de veículos e rotas de coleta de resíduos, desenvolvido em Django.

## Funcionalidades

### Gestão de Veículos
- **Cadastro de Veículos** com os seguintes campos:
  - Placa (formato antigo: ABC1234 ou Mercosul: ABC1D23)
  - Tipo (Compactador ou Caçamba)
  - Número do caminhão
  - Status (Ativo/Inativo)

### Gestão de Rotas
- **Cadastro de Rotas** com os seguintes campos:
  - Veículo responsável
  - Local da coleta
  - Data da coleta
  - Horário da coleta
  - Observações (opcional)
  - Status (Concluída/Pendente)

## Estrutura do Projeto

### Modelos
- `Veiculo`: Armazena informações dos veículos
- `Rota`: Armazena informações das rotas de coleta

### Views
- **Veículos**: Lista, detalhes, criar, editar, excluir, toggle status
- **Rotas**: Lista, detalhes, criar, editar, excluir, toggle status

### Templates
- Interface responsiva com Bootstrap
- Filtros e busca
- Paginação
- Confirmação de exclusão
- Toggle de status via AJAX

## Como Usar

### 1. Acesso ao Sistema
- Acesse o dashboard principal
- Clique em "Gestão de Veículos" no menu lateral

### 2. Cadastrar Veículo
- Clique em "Novo Veículo"
- Preencha os campos obrigatórios:
  - Placa (formato correto será validado)
  - Tipo do veículo
  - Número do caminhão
- Marque "Veículo Ativo" se necessário
- Clique em "Cadastrar"

### 3. Cadastrar Rota
- Clique em "Nova Rota" ou acesse a aba "Rotas"
- Preencha os campos:
  - Selecione o veículo responsável
  - Informe o local da coleta
  - Defina data e horário
  - Adicione observações se necessário
- Clique em "Cadastrar"

### 4. Gerenciar Registros
- **Visualizar**: Clique no ícone de olho para ver detalhes
- **Editar**: Clique no ícone de lápis
- **Alterar Status**: Use os botões de toggle (play/pause para veículos, check/undo para rotas)
- **Excluir**: Clique no ícone de lixeira (confirmação será solicitada)

### 5. Filtros e Busca
- Use os campos de busca para encontrar registros específicos
- Filtre por tipo de veículo, status, data, etc.
- Os filtros são combinados para resultados mais precisos

## Validações Implementadas

### Veículos
- Placa única no sistema
- Formato de placa validado (antigo ou Mercosul)
- Número do caminhão único

### Rotas
- Veículo deve estar ativo
- Combinação única de veículo, data e horário
- Validação de campos obrigatórios

## Tecnologias Utilizadas
- Django 5.2.7
- Bootstrap 4 (SB Admin 2)
- Font Awesome
- MySQL
- JavaScript (AJAX para toggle de status)

## Estrutura de Arquivos
```
app_veiculo/
├── models.py          # Modelos Veiculo e Rota
├── views.py           # Views para CRUD
├── forms.py           # Formulários Django
├── admin.py           # Configuração do admin
├── urls.py            # URLs do app
└── templates/
    └── app_veiculo/
        ├── veiculo_list.html
        ├── veiculo_form.html
        ├── veiculo_detail.html
        ├── veiculo_confirm_delete.html
        ├── rota_form.html
        ├── rota_detail.html
        └── rota_confirm_delete.html
```

## URLs Disponíveis
- `/veiculos/` - Lista de veículos
- `/veiculos/veiculo/create/` - Novo veículo
- `/veiculos/veiculo/<id>/` - Detalhes do veículo
- `/veiculos/veiculo/<id>/update/` - Editar veículo
- `/veiculos/veiculo/<id>/delete/` - Excluir veículo
- `/veiculos/rotas/` - Lista de rotas
- `/veiculos/rota/create/` - Nova rota
- `/veiculos/rota/<id>/` - Detalhes da rota
- `/veiculos/rota/<id>/update/` - Editar rota
- `/veiculos/rota/<id>/delete/` - Excluir rota

## Próximos Passos Sugeridos
1. Implementar relatórios de rotas por período
2. Adicionar notificações para rotas pendentes
3. Implementar dashboard com estatísticas
4. Adicionar exportação de dados (Excel/PDF)
5. Implementar sistema de permissões por usuário
