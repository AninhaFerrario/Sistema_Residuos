PROJETO - COLETA EFICAZ DE RESÍDUOS URBANOS Enganheria de Descarte

Documentos constando na pasta do projeto

1 - Link Figma - [https://www.figma.com/proto/Sd3FSDB82dyEBDxq52Rc3d/Untitled?node-id=1-76&starting-point-node-id=1%3A76&locale=pt-br&t=EmGLsldoXqkiu9zk-1]

2 - Banco de dados em três formatos: a - sql; b - txt; c - Modelo lógico.

3 - Documento - Engenharia do Descarte

4 - Link do sistema - [https://anaroberta2025.pythonanywhere.com/]

Credenciais: 
Administrador - Login: arferrario@gmail.com 
Gestor- Login: gmnatanael24@gmail.com
Usuário - Login: gabriel@gmail.com

Senhas iguais para todas credenciais : Ed109016-0

5 - Descrição completa do sistema

Sistema de Gestão de Coleta de Resíduos

O sistema de gestão da coleta de resíduos foi criado para facilitar o controle e a organização de todo o processo da coleta urbana. Ele funciona como uma plataforma web onde dá para gerenciar usuários, veículos, Pontos de Coletas, problemas operacionais e relatórios gerais, tudo em um só lugar, de um jeito simples, prático e fácil de usar. Além disso, os caminhões são equipados com um chip de monitoramento, responsável por transmitir automaticamente todas as informações dos Pontos de Coletas de resíduos, horários e demais dados operacionais diretamente para o sistema, garantindo maior precisão, rastreabilidade e controle das operações. A base do sistema foi feita com Django, usando MySQL como banco de dados, e a interface é construída com HTML, CSS e Bootstrap.
Por dentro, o sistema segue o modelo clássico do Django: tem modelos para representar os dados, views que cuidam das ações e das páginas, templates que mostram a interface, formulários para inserir dados e decoradores para garantir que cada usuário tenha as permissões certas. Quando alguém entra em uma página, o Django identifica a URL, chama a função certa, consulta o banco de dados, se precisar, e entrega a página pronta para o usuário ver e usar. Para começar a usar, basta instalar o Python, criar um ambiente virtual, instalar as dependências e configurar o MySQL. Depois, é só rodar as migrações e criar um superusuário para começar a usar o sistema normalmente, abrindo o servidor padrão do Django. A partir daí, tudo já está disponível no navegador.

O sistema foi dividido em módulos. No app de usuários, cada pessoa registrada já ganha um perfil vinculado ao usuário padrão do Django. Existem três perfis principais: cidadão, gestor de Sistema de Coleta de Resíduos urbanos e administrador. Cada um tem seu nível de acesso, garantindo que só quem pode faça determinadas ações. O login é feito com email e senha, e o controle de permissões usa decoradores personalizados para liberar ou bloquear o acesso conforme o perfil do usuário. No app de veículos ficam as informações dos caminhões, caçambas e seus Pontos de Coletas. Cada veículo tem seus dados básicos, como placa e tipo. Definem onde e quando a coleta será feita, sempre ligadas a um veículo específico. Tem também um módulo para registrar problemas do serviço, como coletas não realizadas, atrasos e falhas mecânicas. Tudo isso pode ser visto, filtrado, editado ou apagado pelo Admin/gestor.

O sistema ainda tem uma área de relatórios, onde o usuário tem uma visão geral da operação. Dá para ver quantos veículos existem, quantos estão ativos, o total de Ponto de Coleta, quantas foram concluídas e quais problemas foram registrados. Esses dados ajudam a entender como o serviço está indo detectar falhas e tomar decisões mais acertadas. As permissões são organizadas para manter a ordem e a segurança. O cidadão tem acesso básico e pode sinalizar problemas na coleta. O gestor da Engenharia do Descarte tem mais acesso, podendo cadastrar veículos, Pontos de Coletas, horários/dias da semana dos pontos de coletas e gerenciar os problemas. O administrador controla o sistema todo, inclusive os usuários. Essa divisão ajuda a manter a organização e evitar mudanças indevidas.
Na prática, o fluxo é simples. O usuário entra na página de login, coloca email e senha e, se estiver tudo certo, vai para o painel principal. Aí, gestores e administradores podem cadastrar novos veículos, criar Pontos de Coletas como concluídas ouo não e resolver problemas, assim como podem registrar denúncias de coletas. Já os cidadãos conseguem registrar situações, como coletas não realizadas, ajudando a equipe a acompanhar o que está acontecendo pela cidade.

Para colocar o nosso sistema de gestão de coleta de resíduos online, usamos o PythonAnywhere, que é um serviço de hospedagem próprio para aplicações Python, incluindo projetos feitos com Django. O processo foi simples e seguiu alguns passos básicos.
Primeiro, criamos uma conta no PythonAnywhere e fizemos o upload do nosso projeto Django para o ambiente deles. Isso pode ser feito enviando os arquivos diretamente ou conectando o repositório via GitHub. Depois que o código estava lá, criamos um virtual environment dentro do PythonAnywhere para instalar as mesmas dependências que usamos no desenvolvimento, como Django e outros pacotes do requirements.txt.

Em seguida, configuramos o arquivo WSGI, que é responsável por ligar o nosso código Django ao servidor web do PythonAnywhere. Também apontamos a variável DJANGO_SETTINGS_MODULE para o nosso arquivo de configurações. Ajustamos ainda os caminhos para os arquivos estáticos, rodando o collectstatic para que o PythonAnywhere pudesse servir o CSS, JavaScript e imagens corretamente.

Como nosso banco de dados era MySQL, configuramos no PythonAnywhere as mesmas credenciais e apontamos no settings.py para o banco remoto. Depois disso, rodamos as migrações diretamente no console bash do PythonAnywhere para criar as tabelas no banco hospedado.
Por fim, reiniciamos a aplicação no painel web. Quando o servidor carregou, o sistema já estava disponível em um endereço online fornecido pelo PythonAnywhere. Com isso, qualquer pessoa pôde acessar o sistema pelo navegador, sem precisar instalar nada localmente.
