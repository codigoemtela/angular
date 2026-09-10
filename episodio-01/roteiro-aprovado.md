# Introdução ao Angular

## 01 O pedido que precisa virar uma aplicação

> CENA: Helena, Rodrigo e Lia. Entram três pedidos fictícios por mensagem, e-mail e conversa. As mensagens aparecem uma por vez, com frases curtas. Helena reúne os pedidos diante do quadro da sprint. Na primeira fala de cada personagem, mostrar nome e função.

@HELENA: Preciso da ajuda de vocês. Hoje, quando alguém tem um problema com um sistema da empresa, pede ajuda por mensagem, por e-mail ou encontra alguém no corredor. Depois vem a pergunta: quem está cuidando disso? A pessoa que pediu não sabe. A equipe de atendimento precisa procurar a conversa. E às vezes o mesmo problema chega para duas pessoas.

@LIA: Acho que conheço esse sistema. A tela principal é uma conversa com cento e cinquenta mensagens.

@HELENA: E a busca depende de lembrar quem respondeu! Queremos dar ao colaborador um lugar para registrar a solicitação e acompanhar o atendimento. A equipe precisa enxergar uma fila organizada, assumir os pedidos e informar o andamento.

> TELA: Card SOL 01 Registrar uma solicitação. Necessidade: o colaborador registra um pedido e recebe um protocolo para acompanhá-lo. O card permanece em A fazer. Mostrar uma maquete simples com título, descrição e botão Enviar solicitação.

@PROF. RODRIGO: Esse será o projeto da nossa formação: uma central de solicitações internas. Bem-vindo ao Código em Tela. Eu sou o professor Rodrigo, e você vai acompanhar a construção como parte desta equipe. Vamos partir das necessidades da Helena, nossa PO, discutir as dúvidas e transformar os cards em funcionalidades.

@LIA: Para esse primeiro card, basta criar os campos e fazer o botão salvar?

@PROF. RODRIGO: Esse é o começo da conversa. Se a resposta demorar, o que aparece? Se o registro falhar, o texto desaparece? Quem pode consultar esse pedido depois? Nosso formulário já está pedindo algumas decisões.

@HELENA: E eu quero conseguir conferir a entrega. O colaborador precisa saber que o pedido foi registrado e como encontrá-lo depois.

@PROF. RODRIGO: É nesse tipo de aplicação que vamos estudar Angular. Ele é um framework de desenvolvimento web: oferece recursos e convenções para construir e organizar aplicações. Nesta primeira aula, você vai entender o que ele se propõe a resolver e como chegou à forma que usamos hoje. Ao final, vamos voltar a esse card e analisar uma situação juntos.

> TRANSIÇÃO: Vinheta curta do Código em Tela, quatro segundos. Título na tela: Introdução ao Angular.

## 02 Como vamos aprender nesta formação

> CENA: Rodrigo e Davi diante do quadro. Lia entra na segunda metade da conversa. Identificar Davi como Scrum Master. Mostrar apenas um card em destaque.

@DAVI: Vou ajudar a equipe a organizar essas conversas e perceber o que está dificultando o trabalho. Os cards vão acompanhar as entregas. Algumas demandas vão atravessar mais de uma aula, porque precisamos de tempo para entender, construir e verificar.

@PROF. RODRIGO: Nosso objetivo é que você consiga receber uma demanda, esclarecer os critérios e implementar uma solução Angular. Isso envolve ler código, consultar documentação e investigar quando alguma coisa dá errado. Você verá a nossa implementação e também terá desafios para resolver com suas próprias decisões.

@LIA: E quem ainda não conhece HTML, CSS e JavaScript consegue começar por aqui?

@PROF. RODRIGO: Consegue acompanhar esta introdução. Para construir a aplicação nas aulas práticas, esses fundamentos serão necessários. Teremos um curso completo de HTML, CSS e JavaScript em uma formação própria. Aqui faremos uma revisão aplicada, para retomar o que vamos usar e ajudar você a perceber o que precisa estudar melhor.

@PROF. RODRIGO: Se funções, objetos, eventos ou organização de uma página ainda forem assuntos novos, reserve tempo para essa base. Você pode avançar no seu ritmo. Compreender o JavaScript vai ajudar muito quando chegarmos ao TypeScript e ao comportamento dos componentes.

@DAVI: E podemos pausar o vídeo, testar uma ideia e voltar. O andamento da história não precisa ser o ritmo de estudo de cada pessoa.

@PROF. RODRIGO: Exatamente. O código de referência ficará no meu GitHub, e você poderá manter sua implementação no seu próprio repositório. Hoje, basta acompanhar os exemplos e anotar suas respostas. Vamos começar pelo que acontece entre preencher um formulário e receber uma confirmação.

## 03 O que fica difícil quando a interface cresce

### A tela também precisa representar a espera

> CENA: Rodrigo, Lia e Caio. Identificar Caio como desenvolvedor com experiência em JavaScript. A maquete mostra uma solicitação sobre acesso à impressora. Exibir Preenchendo, Enviando e Registro confirmado em momentos distintos. Estes rótulos representam o envio do formulário, não o status do atendimento.

@CAIO: Eu consigo criar esse formulário com HTML, cuidar da aparência com CSS e usar JavaScript para enviar os dados. Onde o Angular entra?

@PROF. RODRIGO: Você consegue, sim. Antes de olhar a contribuição do Angular, vamos localizar as partes. Chamamos de frontend a parte da aplicação com a qual a pessoa interage no navegador. Nossa central também terá um programa no servidor para receber operações, verificar regras e guardar os pedidos. A API é a interface de comunicação que esse programa oferece ao frontend.

@LIA: Então clicar em enviar começa uma conversa entre essas partes.

@PROF. RODRIGO: Isso. A interface envia uma requisição, e a API devolve uma resposta. Na nossa formação, você poderá executar as duas partes no seu computador. Essa separação de responsabilidades continua existindo mesmo quando elas estão na mesma máquina. Agora vamos acompanhar essa conversa pela perspectiva de quem está preenchendo o pedido.

@PROF. RODRIGO: A pessoa preencheu a descrição e clicou em enviar. O pedido saiu, mas a resposta ainda não voltou. Nesse intervalo, a interface precisa representar que há uma operação em andamento.

@LIA: Podemos mudar o texto do botão para Enviando e evitar um segundo clique.

@PROF. RODRIGO: Boa decisão para esse fluxo. Quando chegar a confirmação, mostramos o protocolo. Se houver uma falha, precisamos explicar a situação e preservar o que foi preenchido. Agora temos dados que influenciam a apresentação: o texto digitado, a indicação de envio, a resposta recebida e uma possível mensagem de erro.

@PROF. RODRIGO: Chamamos de estado as informações que descrevem a situação da aplicação em determinado momento. O filtro selecionado é estado. O pedido aberto na tela também. Estar aguardando uma resposta é outro exemplo. Quando essas informações mudam, a interface precisa acompanhar de maneira coerente.

@CAIO: Eu poderia guardar esses valores e escrever funções que atualizam os elementos da página.

@PROF. RODRIGO: Poderia. O cuidado é manter essas atualizações corretas em todos os caminhos. No sucesso, o indicador de espera precisa parar. No erro, também. Ao tentar novamente, a mensagem anterior precisa ser tratada. Conforme surgem mais interações, cresce a quantidade de relações que o código precisa expressar.

> PAUSA: Oito segundos. Mostrar a pergunta Por que o botão continua em Enviando depois de uma falha? A resposta visual só aparece após a fala seguinte.

@LIA: Talvez alguém tenha programado a mudança do botão só no caminho em que tudo dá certo.

@PROF. RODRIGO: Essa é uma hipótese que podemos investigar. Repare como entender os estados já ajuda a formular uma pergunta útil sobre o erro. Ainda não precisamos conhecer os comandos do Angular para raciocinar sobre esse comportamento.

### Uma mudança pode aparecer em vários lugares

> TELA: A mesma solicitação aparece na lista e no painel de detalhes, com o mesmo protocolo. Seu status passa de Aberta para Em atendimento depois de uma confirmação ilustrativa da API. Destacar apenas o registro correspondente. Não mostrar contadores globais ou sincronização entre computadores.

@PROF. RODRIGO: Vamos olhar outro momento do produto. Um atendente assume uma solicitação, e o sistema confirma a mudança. A lista precisa apresentar o novo status. Se os detalhes dessa mesma solicitação estiverem visíveis, também precisam refletir a informação confirmada.

@CAIO: Se cada trecho da tela guardar uma cópia independente, uma delas pode ficar desatualizada.

@PROF. RODRIGO: Isso. Precisamos decidir onde a informação é mantida e como chega a quem depende dela. Angular oferece mecanismos para representar essas relações. A organização do estado continua sendo uma decisão nossa. E há outra distinção: atualizar partes desta aplicação é diferente de receber, em tempo real, uma alteração feita em outro computador.

@LIA: Então usar Angular não faz todos os usuários receberem automaticamente as mudanças?

@PROF. RODRIGO: Não. A aplicação precisa buscar ou receber os dados atualizados por algum mecanismo de comunicação. Depois disso, organizamos como a informação aparece na interface. Vamos estudar cada responsabilidade no momento adequado.

### Manter o produto envolve a equipe inteira

> CENA: Rodrigo, Bia e Rafael. Identificar Bia como UX e Rafael como QA. Mostrar três exemplos de mensagem: confirmação, campo incompleto e falha de envio. Não diferenciar os estados somente por cor.

@BIA: Tenho uma pergunta sobre aquela falha de envio. O que a pessoa vai conseguir entender? Uma mensagem vermelha dizendo Erro pode deixar o usuário sem saber se perdeu o texto ou se deve tentar novamente.

@PROF. RODRIGO: Precisamos definir a mensagem e a próxima ação possível. Também precisamos apresentar isso de forma acessível. A cor pode ajudar, mas o conteúdo da mensagem precisa comunicar o que aconteceu.

@RAFAEL: E eu quero verificar mais de um caminho. Vou preencher corretamente, enviar com um campo obrigatório vazio e observar o comportamento quando o serviço estiver indisponível. Se testarmos apenas a confirmação, muita coisa pode passar despercebida.

@PROF. RODRIGO: Essas perguntas ajudam a escrever os critérios antes da implementação. Conforme o sistema cresce, várias pessoas vão trabalhar nas mesmas telas. Se copiarmos a apresentação de status em cinco lugares, uma mudança de texto pode exigir cinco correções. Se cada tela tratar os erros de um jeito, a experiência fica inconsistente.

@BIA: Podemos compartilhar uma apresentação quando ela tiver o mesmo significado. Mas duas coisas parecidas podem precisar de comportamentos diferentes.

@PROF. RODRIGO: Exato. Reaproveitar exige entender a responsabilidade daquele trecho. O Angular nos dá uma estrutura para construir partes da interface e combiná-las. Isso ajuda na manutenção, mas ainda precisamos escolher bons limites e conversar sobre as regras do produto.

> BASE TÉCNICA: [Visão geral do Angular](https://angular.dev/overview); [Composição com componentes](https://angular.dev/essentials/components); [Estado e reatividade com signals](https://angular.dev/essentials/signals). As situações da central são exemplos originais da formação.

## 04 A história do Angular e as mudanças de geração

### O início do AngularJS

> CENA: Rodrigo e Caio. Linha do tempo com 2009 Início do projeto e AngularJS Primeira geração. A tela histórica deve ter indicação de contexto, sem instruções de instalação. Não usar o logotipo moderno como se fosse o original.

@PROF. RODRIGO: Para entender essa proposta, vamos voltar à origem do AngularJS. Miško Hevery começou o projeto em 2009. A iniciativa se desenvolveu com a participação do Google e da comunidade. O problema que estamos discutindo já estava presente: construir interfaces interativas e manter a apresentação relacionada aos dados da aplicação.

@CAIO: Era a época em que muita gente usava jQuery para encontrar elementos e responder aos cliques.

@PROF. RODRIGO: Esse era um caminho bastante conhecido. Pense na diferença entre escrever uma sequência de comandos para alterar uma mensagem e declarar de qual dado aquela mensagem depende. AngularJS apostou em estender o HTML com recursos para descrever interfaces dinâmicas. Essa maneira de expressar o resultado é chamada de declarativa.

@PROF. RODRIGO: Vamos usar um exemplo pequeno. Há um campo para o título da solicitação e uma prévia logo abaixo. A prévia precisa mostrar o título que a pessoa está preenchendo. Em uma descrição declarativa, registramos essa relação no modelo da interface. O framework participa da atualização quando o dado muda.

> TELA: Campo Título e uma prévia do mesmo título. Digitar Acesso à impressora lentamente. Setas discretas relacionam Campo, Dado título e Prévia. Manter essa relação legível por dez segundos antes de trocar de quadro.

@CAIO: Esse modelo da interface é o template?

@PROF. RODRIGO: Sim. Nesse contexto, template é o modelo usado para construir a apresentação, com HTML e instruções que relacionam a tela aos dados. Essa ligação é chamada de data binding. O AngularJS ficou muito associado ao two-way data binding, ou ligação em duas direções: editar o campo pode atualizar o modelo, e alterar o modelo pode atualizar o campo.

@PROF. RODRIGO: A ligação depende de como o programa foi escrito. Não significa que qualquer variável esteja conectada a qualquer parte da página. Também não envia automaticamente o conteúdo ao banco. Estamos falando da relação entre dados e interface.

> BASE HISTÓRICA: [Entrevista com Miško Hevery sobre a origem do AngularJS](https://www.youtube.com/watch?v=X0VsStcCCM8); [Proposta e recursos do AngularJS](https://angularjs.org/).

### O que essa proposta mudou no trabalho

> CENA: Rodrigo, Caio e Marina. Identificar Marina como desenvolvedora de sistemas corporativos. Comparar duas descrições em português: Procurar o elemento e trocar seu texto e A prévia apresenta o título informado. Nenhuma das descrições deve parecer código executável.

@MARINA: Então a equipe passava a descrever melhor as relações da tela, em vez de distribuir as alterações por vários eventos?

@PROF. RODRIGO: Essa é uma forma de entender a mudança de abordagem. No nosso exemplo, fica explícito que a prévia depende do título. Quando uma pessoa entra na equipe, ela pode procurar essa relação no template e no código que mantém o dado. Isso facilita discutir a intenção da implementação.

@CAIO: Mas o programador ainda precisa decidir quando enviar, como tratar um erro e o que fazer com a resposta.

@PROF. RODRIGO: Precisa. A programação declarativa da interface não elimina as demais decisões. Você continua escrevendo comportamento. O benefício é poder expressar certas relações diretamente, sem repetir cada operação visual em todos os lugares que alteram os mesmos dados.

@MARINA: Também precisamos pensar nas dependências. A tela vai conversar com algo que busca ou registra a solicitação.

@PROF. RODRIGO: AngularJS já trazia serviços e injeção de dependências. A ideia era organizar responsabilidades e fornecer a uma parte do programa aquilo de que ela precisava. Esses conceitos ajudavam a estruturar aplicações e a substituir dependências durante testes. Eles continuariam importantes na história do Angular.

@PROF. RODRIGO: Se você encontrar um tutorial com controllers e dólar scope, terá pistas de que o exemplo pertence ao AngularJS. Vamos reconhecer esses nomes para identificar a geração do material. Não será necessário estudar todas essas APIs antigas para começar nossa implementação.

> BASE TÉCNICA: [Guia histórico de migração e diferenças entre AngularJS e Angular](https://v2.angular.io/docs/ts/latest/guide/upgrade.html); [Injeção de dependências no Angular](https://angular.dev/guide/di).

### A reescrita que levou ao Angular 2

> TELA: Separar AngularJS Versões 1.x de Angular Versões 2 em diante. Na segunda família, destacar 2016 Angular 2. Uma transição visual indica mudança de geração, não uma atualização automática da mesma aplicação.

@PROF. RODRIGO: Em setembro de 2016, foi lançada a versão final do Angular 2. Essa passagem marcou uma reescrita do framework. A arquitetura foi reorganizada em torno da composição por componentes, e o TypeScript passou a ter um papel central na forma de desenvolver com Angular.

@MARINA: Se uma empresa tinha um sistema em AngularJS, bastava atualizar o pacote para continuar?

@PROF. RODRIGO: Não. Havia diferenças nas APIs e na organização do código. Migrar exigia trabalho planejado. A própria equipe do Angular disponibilizou recursos para permitir uma transição gradual, com partes antigas e novas convivendo enquanto a aplicação era adaptada.

@MARINA: Isso faz diferença para quem precisa manter o atendimento funcionando durante a mudança. Não dá para interromper todos os pedidos enquanto a equipe reescreve as telas.

@PROF. RODRIGO: E essa é uma consequência importante da história. Uma escolha técnica também cria compromissos de manutenção. Ao avaliar uma migração, precisamos considerar o que existe, como verificar os fluxos e como realizar a transição. Uma aplicação continuar abrindo é apenas uma parte dessa verificação.

@CAIO: Então AngularJS e Angular não são dois nomes intercambiáveis para o mesmo código.

@PROF. RODRIGO: Isso. AngularJS identifica a família um. Angular, sem JS no final, identifica a família que começou na versão dois. Você também pode encontrar a expressão Angular dois ou superior. Nossa formação trabalhará com essa família moderna.

@MARINA: E a notícia de que o suporte tinha acabado?

@PROF. RODRIGO: O suporte oficial ao AngularJS foi encerrado no fim de 2021, com o comunicado publicado em janeiro de 2022. Isso não fez as aplicações pararem de funcionar naquele dia, mas encerrou aquele suporte oficial. A informação se refere ao AngularJS, e precisa ser distinguida da evolução do Angular moderno.

> BASE HISTÓRICA: [Lançamento do Angular 2 no histórico oficial](https://github.com/angular/angular/blob/main/CHANGELOG_ARCHIVE.md#200-proprioception-reinforcement-2016-09-14); [Guia de migração do AngularJS para Angular](https://v2.angular.io/docs/ts/latest/guide/upgrade.html); [Encerramento do suporte oficial ao AngularJS](https://blog.angular.dev/discontinued-long-term-support-for-angularjs-cc066b82e65a).

### A evolução depois da reescrita

> CENA: Rodrigo e Lia. Mostrar um marco por vez. 2020 Angular 9 e Ivy. 2022 Componentes standalone. 2023 Signals e novos templates. Deixar a relação de cada marco com seu propósito visível, sem uma lista de todas as versões.

@PROF. RODRIGO: A história continuou depois de 2016. Em 2020, Angular 9 passou a usar Ivy por padrão. Ivy é uma infraestrutura de compilação e execução do framework. Compilar envolve preparar e transformar o código para execução. Essa infraestrutura também participa da produção e atualização da interface. A mudança trouxe avanços nas ferramentas e na maneira de preparar a aplicação.

@LIA: Eu preciso entender esse funcionamento interno para criar meu primeiro componente?

@PROF. RODRIGO: Não. Aqui, vale reconhecer que um framework também evolui por dentro. Algumas mudanças aparecem diretamente no código que escrevemos. Outras melhoram a infraestrutura que transforma esse código e o faz funcionar.

@PROF. RODRIGO: Em 2022, Angular 14 apresentou os componentes standalone como uma prévia. Angular 15 tornou essas APIs estáveis. A proposta foi reduzir a necessidade de NgModules na composição das aplicações. Isso permitiu declarar dependências de componentes de uma maneira mais direta.

@LIA: Standalone quer dizer que o componente não depende de ninguém?

@PROF. RODRIGO: O nome pode sugerir isso, mas ele pode depender de outros componentes e serviços. A mudança está na forma de declarar e organizar essas dependências. Se você encontrar uma aplicação organizada com NgModules, está vendo uma abordagem que faz parte da história do Angular e que ainda aparece em bases existentes.

@PROF. RODRIGO: Em 2023, Angular 16 introduziu uma prévia dos signals. Um signal representa um valor que pode participar de relações reativas. Podemos, por exemplo, representar um título e fazer a apresentação depender dele. Ao atualizar esse valor pelos mecanismos adequados, o Angular consegue acompanhar as partes que dependem dele e precisam reagir.

@LIA: Isso se relaciona com a nossa conversa sobre manter os dados e a tela coerentes.

@PROF. RODRIGO: Sim. E no mesmo ano, Angular 17 apresentou uma nova sintaxe para condições e repetições nos templates, inicialmente como prévia, além da nova documentação em angular ponto dev. São mudanças na experiência de escrever e aprender Angular. Não precisamos percorrer todas as versões para reconhecer essa direção.

@PROF. RODRIGO: Os marcos continuam depois dessa linha do tempo. Quando formos preparar o ambiente, usaremos versões definidas no material da formação. Ao consultar um exemplo externo, confira a versão e a documentação correspondente. Isso evita juntar instruções de momentos diferentes e interpretar toda diferença como um erro seu.

> BASE HISTÓRICA: [Angular 9 e Ivy](https://blog.angular.dev/version-9-of-angular-now-available-project-ivy-has-arrived-23c97b63cfa3); [Angular 14 e standalone em prévia](https://blog.angular.dev/angular-v14-is-now-available-391a6db736af); [Angular 15 e standalone estável](https://blog.angular.dev/angular-v15-is-now-available-df7be7f2f4c8); [Angular 16 e signals](https://blog.angular.dev/angular-v16-is-here-4d7a28ec680d); [Angular 17 e templates](https://blog.angular.dev/introducing-angular-v17-4d7033312e4b).

## 05 Como o Angular ajuda a organizar nossa central

### Componentes e responsabilidades

> CENA: Rodrigo e Lia. Retomar a mesma maquete da central. Destacar, sucessivamente, o formulário, a lista e o indicador de status. Não dividir cada palavra ou ícone em um componente.

@PROF. RODRIGO: Podemos agora dar uma definição com contexto. Angular é um framework de código aberto para construir aplicações web, mantido por uma equipe no Google com participação da comunidade. Ele oferece uma estrutura para organizar a interface, as dependências e o comportamento, acompanhada de ferramentas e bibliotecas para tarefas frequentes.

@LIA: Qual é a diferença entre isso e usar uma biblioteca?

@PROF. RODRIGO: Pense no grau de organização oferecido. Uma biblioteca costuma fornecer recursos que você chama dentro da estrutura que escolheu. Um framework também estabelece convenções e participa da execução da aplicação. Em Angular, escrevemos componentes seguindo seu modelo, e o framework coordena como eles entram na interface e respondem às mudanças.

@PROF. RODRIGO: Um componente representa uma parte da interface com uma responsabilidade definida. Podemos ter um componente para apresentar o status de uma solicitação e usá-lo na lista e nos detalhes. Cada uso recebe a informação correspondente. Se alterarmos a apresentação compartilhada, conseguimos manter esses lugares coerentes.

@LIA: E o que existe dentro de um componente?

@PROF. RODRIGO: Há um template para descrever a apresentação e código para os dados e comportamentos. Podemos associar estilos àquele componente. No nosso trabalho, você verá HTML, CSS e TypeScript participando dessa construção. Por isso a base da web continua presente quando adotamos Angular.

@LIA: Eu separaria o formulário da listagem, porque eles têm interações diferentes. Mas não criaria um componente para cada palavra só para aumentar a quantidade.

@PROF. RODRIGO: É um bom ponto de partida. Ao implementar, vamos avaliar essas divisões pelo comportamento e pelas mudanças que precisamos fazer. A possibilidade de criar componentes nos ajuda a organizar o código; o tamanho adequado depende da responsabilidade.

> BASE TÉCNICA: [Definição do Angular](https://angular.dev/overview); [Composição e estrutura dos componentes](https://angular.dev/essentials/components).

### Serviços e comunicação com a API

> CENA: Rodrigo e Marina. Mostrar Formulário, Serviço de solicitações e API em uma sequência compacta. Abaixo da API, indicar Dados persistidos. Na volta, mostrar uma resposta de confirmação. As setas ilustram responsabilidades, sem sugerir que um serviço Angular seja um servidor.

@MARINA: Onde colocamos o código que conversa com a API? Eu não gostaria de repetir os detalhes da comunicação em cada tela.

@PROF. RODRIGO: Podemos concentrar essa responsabilidade em um serviço Angular. Por exemplo, um serviço de solicitações pode oferecer operações para consultar e registrar pedidos. Os componentes usam essas operações sem precisar duplicar todos os detalhes da chamada.

@PROF. RODRIGO: A injeção de dependências permite fornecer esse serviço a quem precisa dele. O componente declara a dependência, e o sistema de injeção resolve o fornecimento conforme a configuração. Mais adiante vamos ver isso no código e entender como essa organização também ajuda nos testes.

@MARINA: E esse serviço Angular não é a própria API.

@PROF. RODRIGO: Correto. Aqui ele faz parte do frontend. A API é outra parte do sistema, que recebe as requisições e executa operações no servidor. O Angular oferece o HttpClient para organizar a comunicação HTTP. Ainda precisamos decidir quais dados enviar, como interpretar a resposta e como tratar uma falha.

@PROF. RODRIGO: Nossa API em Node será fornecida pronta, com instruções para execução. Durante a formação, vamos aprender a consumi-la pelo Angular. Quando a pessoa registrar uma solicitação, será a API que validará aquela operação e cuidará da persistência no banco. A interface exibirá o resultado recebido.

@MARINA: Isso permite estudar o frontend com uma integração concreta, mantendo claro o contrato entre as partes.

@PROF. RODRIGO: Exatamente. O contrato descreve o que a API espera e o que devolve. Se ele mudar, precisamos avaliar a integração. Ter uma separação de responsabilidades torna mais fácil localizar o trabalho necessário.

> BASE TÉCNICA: [Injeção de dependências](https://angular.dev/guide/di); [Comunicação HTTP](https://angular.dev/guide/http).

### Navegação e ferramentas que trabalham juntas

> CENA: Rodrigo e Caio. A maquete alterna entre lista e detalhes. O endereço fictício muda de /solicitacoes para /solicitacoes/1042. Depois mostrar um campo e a indicação Campo obrigatório. Não apresentar comandos de instalação.

@CAIO: E navegar da lista para os detalhes? É outra biblioteca que a equipe precisa escolher?

@PROF. RODRIGO: Angular oferece um roteador oficial. Ele relaciona os endereços às partes da aplicação e permite organizar a navegação. Também há recursos para formulários, validação e carregamento de partes do código sob demanda, que você vai encontrar pelo nome lazy loading.

@PROF. RODRIGO: Uma aplicação pode trocar a tela dentro do navegador sem recarregar um documento inteiro a cada navegação. Você verá isso associado à expressão single-page application, ou SPA. Isso não quer dizer que o produto tenha uma única tela ou um único endereço.

@CAIO: E Angular só funciona dessa maneira?

@PROF. RODRIGO: Ele também oferece renderização no servidor e geração de páginas estáticas. A estratégia depende do produto. Nossa primeira preocupação será compreender a interface interativa da central. Depois podemos avaliar as necessidades de publicação sem confundir Angular com uma única forma de entregar páginas.

@PROF. RODRIGO: Na prática, usaremos o VS Code e as ferramentas do Angular para criar e trabalhar no projeto. TypeScript ajudará a descrever os tipos dos dados e identificar certas inconsistências durante o desenvolvimento. Ele se apoia no JavaScript, e seu uso não substitui validar o que chega de fora da aplicação.

@CAIO: Então podemos ter apoio das ferramentas e ainda assim precisar conferir o resultado em execução.

@PROF. RODRIGO: Sim. Essa combinação fará parte do treinamento. Vamos usar o que as ferramentas oferecem e observar o comportamento que a demanda exige.

> BASE TÉCNICA: [Navegação com o roteador Angular](https://angular.dev/guide/routing); [Formulários](https://angular.dev/guide/forms); [Renderização no servidor e estratégias híbridas](https://angular.dev/guide/ssr); [TypeScript e JavaScript](https://www.typescriptlang.org/docs/handbook/typescript-from-scratch.html).

## 06 O que continua sendo responsabilidade da equipe

> CENA: Rodrigo, Bia e Rafael. Mostrar a mesma solicitação vista por um solicitante e por um atendente. Os dados pessoais são fictícios. O solicitante vê seus próprios pedidos; a equipe de atendimento vê a fila autorizada.

@RAFAEL: Se usarmos Angular, a aplicação já fica segura?

@PROF. RODRIGO: Angular oferece recursos de proteção, mas a segurança depende da implementação inteira. Na nossa central, esconder um botão pode orientar a interface, mas a API também precisa verificar se a pessoa está autorizada a executar a operação. Um pedido enviado diretamente ao servidor não pode ignorar essa regra.

@RAFAEL: Então eu verificaria a permissão na operação, além de observar o que aparece na tela.

@PROF. RODRIGO: Sim. Quando estudarmos autenticação, separaremos identificação, permissões e navegação. O frontend participa dessa experiência, e o servidor precisa aplicar os controles de acesso. Esse princípio já deve fazer parte da maneira como pensamos o produto.

@BIA: E a interface não fica clara só porque os componentes estão organizados. Ainda precisamos cuidar dos textos, da navegação por teclado e do que acontece quando a pessoa não consegue concluir uma ação.

@PROF. RODRIGO: Também precisaremos cuidar do desempenho, das dependências e da manutenção. Uma ferramenta oferece possibilidades. Para usá-las bem, avaliamos a necessidade e verificamos o resultado. Em um site pequeno com poucas interações, talvez uma estrutura mais simples seja suficiente. Na nossa central, vamos explorar Angular porque teremos várias telas, estados, integrações e responsabilidades compartilhadas.

@BIA: E podemos aprender o motivo de uma escolha, para depois avaliar outro projeto com mais critério.

@PROF. RODRIGO: Esse é o objetivo. Ao justificar uma decisão, procure relacioná-la a um problema observável: duplicação de comportamento, dificuldade de manutenção, informação inconsistente ou uma necessidade de uso. Assim a conversa técnica ajuda a equipe a decidir o que fazer.

> BASE TÉCNICA: [Controle de navegação e necessidade de autorização no servidor](https://angular.dev/guide/routing/route-guards). A avaliação de adequação ao projeto é uma análise didática aplicada à central.

## 07 Sua primeira análise de uma demanda

> CENA: Helena, Rodrigo, Lia e Rafael. Retomar SOL 01 em A fazer. Mostrar o cenário do exercício em três passos, um por vez: a pessoa escreve a descrição; clica em enviar; aparece uma mensagem de sucesso antes da resposta da API. Em seguida, o serviço informa que o registro falhou.

@HELENA: Vamos conferir o que esperamos desse primeiro pedido. A pessoa precisa registrar a solicitação e receber um protocolo para acompanhá-la. Quero mostrar uma situação para vocês avaliarem.

@PROF. RODRIGO: A pessoa escreveu a descrição e clicou em enviar. A tela limpou os campos e mostrou Solicitação registrada imediatamente. Só depois chegou uma resposta informando que a operação falhou. Pense em três pontos: qual informação a interface apresentou antes da hora? O que deveria aparecer durante a espera? E o que você faria com o texto diante dessa falha?

> PAUSA: Doze segundos. Manter as três perguntas na tela, com espaço suficiente entre elas. Exibir Pause para anotar sua resposta. Não revelar a solução durante a pausa.

@LIA: A tela afirmou que o pedido estava registrado antes de receber a confirmação. Durante a espera, eu mostraria que o envio está em andamento. E manteria o texto disponível se o registro falhasse, para a pessoa poder corrigir ou tentar de novo conforme a orientação.

@RAFAEL: Eu verificaria se a mensagem de sucesso só aparece depois da confirmação, se o protocolo recebido é apresentado e se a falha preserva o preenchimento. Também observaria se o indicador de envio termina nos dois caminhos.

@PROF. RODRIGO: Essas respostas relacionam uma necessidade de uso aos estados e à integração. A interface mantém o preenchimento e apresenta o andamento. A API confirma ou rejeita a operação conforme suas regras. O código precisa lidar com cada resultado. Angular ajuda a organizar essa implementação, e o comportamento esperado vem da demanda que discutimos.

@HELENA: Agora consigo olhar a entrega com critérios mais claros. Uma mensagem bonita não basta se eu não consigo confiar no que ela informa.

> TELA: Para continuar o exercício, mostrar o novo cenário De volta à lista. A pessoa filtra solicitações por status, abre os detalhes e retorna. O filtro desaparece. Perguntas: qual estado foi perdido e como você descreveria o comportamento esperado?

@PROF. RODRIGO: Para praticar sozinho, analise o segundo cenário que está na tela. Escreva qual informação precisa ser preservada e um critério que permita verificar o retorno à lista. Você não precisa implementar ainda. Precisa conseguir explicar a expectativa e como observar se ela foi atendida.

@PROF. RODRIGO: Antes de terminar, responda também com suas palavras: por que estamos usando Angular neste projeto? E como você distinguiria um tutorial de AngularJS de um material da família Angular? Se precisar voltar a um trecho, use os capítulos. O importante é construir uma explicação que faça sentido para você.

## 08 Fechamento e próxima aula

> CENA: Rodrigo e Davi. O card permanece em A fazer, com a anotação Critérios discutidos. Ao lado, apresentar brevemente Dados, Interface e Comportamento. Não mover o card para Concluído, pois a funcionalidade ainda não foi implementada.

@DAVI: Nosso card continua em A fazer. Já entendemos melhor a necessidade e levantamos comportamentos que vamos conferir quando houver uma implementação.

@PROF. RODRIGO: Hoje, você viu por que uma interface com várias interações precisa de organização. Acompanhou a proposta do AngularJS, a mudança de geração em 2016 e alguns marcos da evolução do Angular. Também relacionou componentes, estado e comunicação com a API ao nosso projeto.

@PROF. RODRIGO: Na próxima aula, vamos observar um componente pequeno e acompanhar como uma ação altera um dado e aparece na interface. Vamos aproximar esses conceitos do código, explicando cada parte. Guarde suas respostas do exercício para comparar com as decisões que faremos ao longo da formação.

@PROF. RODRIGO: Se surgir uma dúvida, anote o trecho e tente descrever o que você entendeu e onde a explicação deixou de fazer sentido. Você pode me enviar essa pergunta por mensagem. Obrigado por acompanhar o Código em Tela. Até a próxima aula.

> ENCERRAMENTO: Cartela de quatro segundos com o nome do canal e o tema da próxima aula Como um componente relaciona dados e interface.
