PROJETO - COLETA EFICAZ DE RESÍDUOS URBANOS Enganheria de Descarte

Documentos constando na pasta do projeto

Link Figma - [https://www.figma.com/proto/Sd3FSDB82dyEBDxq52Rc3d/Untitled?node-id=1-76&starting-point-node-id=1%3A76&locale=pt-br&t=EmGLsldoXqkiu9zk-1]

Banco de dados em três formatos: a - sql; b - txt; c - Modelo lógico.

Documento - TAP

Readme.md - Link do Figma

Descrição completa do sistema

Sistema de Gestão de Coleta de Resíduos

O sistema de gestão da coleta de resíduos foi criado para facilitar o controle e a organização de todo o processo da coleta urbana. Ele funciona como uma plataforma web onde dá para gerenciar usuários, 
veículos, rotas, problemas operacionais e relatórios gerais, tudo em um só lugar, de um jeito simples, prático e fácil de usar. A base do sistema foi feita com Django, usando MySQL como banco de dados, e a 
interface é construída com HTML, CSS e Bootstrap.

Por dentro, o sistema segue o modelo clássico do Django: tem modelos para representar os dados, views que cuidam das ações e das páginas, templates que mostram a interface, formulários para inserir dados e
decoradores para garantir que cada usuário tenha as permissões certas. Quando alguém entra em uma página, o Django identifica a URL, chama a função certa, consulta o banco de dados, se precisar, e entrega a 
página pronta para o usuário ver e usar. Para começar a usar, basta instalar o Python, criar um ambiente virtual, instalar as dependências e configurar o MySQL. Depois, é só rodar as migrações e criar um 
superusuário para começar a usar o sistema normalmente, abrindo o servidor padrão do Django. A partir daí, tudo já está disponível no navegador.

O sistema foi dividido em módulos. No app de usuários, cada pessoa registrada já ganha um perfil vinculado ao usuário padrão do Django. Existem três perfis principais: cidadão, gestor de rotas e administrador. 
Cada um tem seu nível de acesso, garantindo que só quem pode faça determinadas ações. O login é feito com email e senha, e o controle de permissões usa decoradores personalizados para liberar ou bloquear o acesso
conforme o perfil do usuário. No app de veículos e rotas ficam as informações dos caminhões, caçambas e seus trajetos. Cada veículo tem seus dados básicos, como placa e tipo. As rotas definem onde e quando a 
coleta será feita, sempre ligadas a um veículo específico. Tem também um módulo para registrar problemas do serviço, como coletas não realizadas, atrasos e falhas mecânicas. Tudo isso pode ser visto, filtrado, 
editado ou apagado pelos gestores.

O sistema ainda tem uma área de relatórios, onde o usuário tem uma visão geral da operação. Dá para ver quantos veículos existem, quantos estão ativos, o total de rotas, quantas foram concluídas e quais problemas 
foram registrados. Esses dados ajudam a entender como o serviço está indo, detectar falhas e tomar decisões mais acertadas. As permissões são organizadas para manter a ordem e a segurança. O cidadão tem acesso 
básico e pode sinalizar problemas na coleta. O gestor de rotas tem mais acesso, podendo cadastrar veículos, rotas e gerenciar os problemas. O administrador controla o sistema todo, inclusive os usuários. Essa 
divisão ajuda a manter a organização e evitar mudanças indevidas.

Na prática, o fluxo é simples. O usuário entra na página de login, coloca email e senha e, se estiver tudo certo, vai para o painel principal. Aí, gestores e administradores podem cadastrar novos veículos, 
criar rotas, marcar rotas como concluídas e resolver problemas. Já os cidadãos conseguem registrar situações, como coletas não realizadas, ajudando a equipe a acompanhar o que está acontecendo pela cidade.
