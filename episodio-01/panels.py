# SPDX-License-Identifier: GPL-3.0-only
"""Exact, original teaching screens for the complete approved episode."""
import functools
import math
from PIL import Image,ImageDraw
import visuals as v
from visuals import text,lines,box,pill,heading,section_card,sol_card,check,font
from visuals import NAVY,TEAL,CORAL,INK,MUTED,LINE,PALE,WHITE

def note(d,value,y=543,color=MUTED):
    lines(d,(427,y),value,18,778,color,leading=24)

def cards(d,entries,visible=None):
    for n,(title,desc) in enumerate(entries):
        if visible is None or n<visible:
            y=188+n*112
            box(d,(426,y,1209,y+98),PALE,16,PALE)
            pill(d,444,y+19,f'{n+1:02d}',WHITE,TEAL,17)
            text(d,(506,y+13),title,23,NAVY,True)
            lines(d,(506,y+47),desc,19,677,MUTED,leading=25)

def definition(d,word,meaning,below=None):
    box(d,(426,190,1209,446),NAVY,20,NAVY)
    size=47
    while font(size,True).getlength(word)>716:size-=1
    text(d,(453,212),word,size,WHITE,True)
    lines(d,(455,294),meaning,25,712,'#E1EBF3',leading=36)
    if below:lines(d,(427,477),below,22,777,INK,leading=31)

def pair(d,left,right,labels=('01','02'),y=188,h=309):
    for n,entry in enumerate((left,right)):
        title,body=entry;x=426+n*401
        box(d,(x,y,x+382,y+h),PALE,18,PALE)
        pill(d,x+20,y+19,labels[n],WHITE,TEAL,14)
        end=lines(d,(x+22,y+68),title,26,338,NAVY,True,34)
        lines(d,(x+22,end+17),body,22,338,MUTED,leading=31)

def arrow(d,points,color=TEAL,width=3):
    d.line(points,fill=color,width=width)
    (x0,y0),(x,y)=points[-2:]
    angle=math.atan2(y-y0,x-x0)
    d.polygon([(x,y),(x-10*math.cos(angle-.5),y-10*math.sin(angle-.5)),
               (x-10*math.cos(angle+.5),y-10*math.sin(angle+.5))],fill=color)

def request_form(d,state='fill',title='Acesso à impressora'):
    x,y,w=426,185,783
    box(d,(x,y,x+w,526),WHITE,18,LINE,2)
    text(d,(449,199),'CENTRAL DE SOLICITAÇÕES',14,NAVY,True)
    text(d,(1186,201),'MAQUETE',12,MUTED,anchor='ra')
    d.line((426,229,1209,229),fill=LINE)
    if state=='success':
        d.ellipse((453,264,497,308),fill=TEAL);check(d,465,278,WHITE)
        text(d,(513,268),'Registro confirmado',27,NAVY,True)
        text(d,(454,337),'Protocolo recebido da API',19,MUTED)
        text(d,(452,373),'SOL-1042',36,TEAL,True)
        text(d,(454,441),'Você pode acompanhar o atendimento.',20,INK)
        return
    text(d,(449,245),'Título',16,INK,True)
    box(d,(448,272,1187,313),'#FAFCFD',8)
    text(d,(462,281),title if state!='empty' else '',19,INK)
    text(d,(449,327),'Descrição',16,INK,True)
    box(d,(448,354,1187,414),'#FAFCFD',8)
    if state!='empty':text(d,(462,368),'Não consigo acessar a impressora do setor.',19,INK)
    if state=='error':
        text(d,(450,428),'Falha no envio. Seu texto foi preservado.',19,'#9B493D',True)
        label='Tentar novamente';color=TEAL;by=465
    elif state=='waiting':label='Enviando…';color='#677D8B';by=449
    elif state=='empty':
        text(d,(450,428),'Título: campo obrigatório.',19,'#9B493D',True)
        label='Enviar solicitação';color=TEAL;by=465
    else:label='Enviar solicitação';color=TEAL;by=449
    box(d,(448,by,706,by+43),color,10,color)
    text(d,(465,by+10),label,19,WHITE,True)
    if state=='waiting':text(d,(730,by+12),'Aguardando a resposta da API',18,MUTED)

def api(d,service=True,response=False):
    # Explicit browser/server boundaries, with storage under the API.
    box(d,(426,188,849,514),'#EFF6F7',18,'#D1E4E7',2)
    text(d,(448,207),'NAVEGADOR · FRONTEND',16,TEAL,True)
    box(d,(449,251,824,337),WHITE,13,LINE)
    text(d,(637,277),'Componente / formulário' if service else 'Interface / formulário',23,NAVY,True,'ma')
    if service:
        arrow(d,[(637,344),(637,373)])
        box(d,(449,381,824,474),WHITE,13,LINE)
        text(d,(637,397),'Serviço de solicitações',23,NAVY,True,'ma')
        text(d,(637,435),'Parte da aplicação Angular',17,MUTED,anchor='ma')
        flow_y=423
    else:
        text(d,(449,391),'A interface envia a requisição.',20,INK)
        text(d,(449,425),'A resposta informa o resultado.',20,INK)
        flow_y=294
    box(d,(944,188,1209,514),'#F6F2F6',18,'#E1D8E2',2)
    text(d,(966,207),'SERVIDOR',16,'#80537D',True)
    box(d,(966,251,1187,339),WHITE,13,LINE)
    text(d,(1076,273),'API',32,NAVY,True,'ma')
    text(d,(1076,315),'Operações e regras',16,MUTED,anchor='ma')
    arrow(d,[(1076,345),(1076,393)],'#80537D')
    box(d,(966,402,1187,482),WHITE,13,LINE)
    text(d,(1076,417),'Banco de dados',22,NAVY,True,'ma')
    text(d,(1076,450),'Dados persistidos',16,MUTED,anchor='ma')
    arrow(d,[(850,flow_y),(890,flow_y),(890,288),(936,288)])
    text(d,(894,246),'HTTP',15,TEAL,True,'ma')
    if response:
        arrow(d,[(935,359),(916,359),(916,491),(857,491)],CORAL)
        text(d,(918,522),'Resposta',16,'#9B493D',True,anchor='ma')
    note(d,'O serviço Angular pertence ao frontend; a persistência fica no servidor.' if service else
         'As responsabilidades continuam separadas quando tudo roda no mesmo computador.',y=553)

def status_sync(d,phase=0,inconsistent=False):
    status='Aberta' if phase==0 else 'Em atendimento'
    for n,label in enumerate(('Lista de solicitações','Detalhes da solicitação')):
        x=426+n*401
        box(d,(x,188,x+382,459),WHITE,18,LINE,2)
        text(d,(x+22,207),label,22,NAVY,True)
        d.line((x,250,x+382,250),fill=LINE)
        text(d,(x+23,276),'SOL-1042',21,TEAL,True)
        lines(d,(x+23,318),'Acesso à impressora',23,333,INK,True)
        value='Aberta' if inconsistent and n==1 else status
        pill(d,x+22,391,value,'#EAF4F3' if value!='Aberta' else '#FFF0D5',TEAL if value!='Aberta' else '#76551F',17)
    if inconsistent:
        note(d,'Exemplo de inconsistência: duas cópias, informações diferentes.',y=491,color='#9B493D')
    else:
        pill(d,426,484,'API: mudança confirmada' if phase else 'Antes da confirmação',
             '#EAF4F3' if phase else PALE,TEAL if phase else MUTED,18)
    note(d,'O mesmo pedido, apresentado em dois lugares da aplicação.',y=548)

def binding(d,phase=20,two_way=False):
    title='Acesso à impressora'[:max(0,min(20,phase))]
    for y,label in [(212,'Campo Título'),(424,'Prévia')]:
        text(d,(427,y-25),label,17,MUTED,True)
        box(d,(426,y,755,y+80),WHITE,12,LINE,2)
        text(d,(441,y+24),title,22,NAVY)
    box(d,(877,297,1209,397),'#EAF4F3',16,'#CCE3E2',2)
    text(d,(899,311),'Dado: título',20,TEAL,True)
    text(d,(899,349),title,22,NAVY)
    arrow(d,[(763,252),(819,252),(819,323),(868,323)])
    arrow(d,[(868,371),(819,371),(819,464),(763,464)])
    text(d,(838,221),'Edição',15,TEAL,True,anchor='ma')
    text(d,(837,486),'Atualização',15,TEAL,True,anchor='ma')
    if two_way:
        arrow(d,[(898,287),(898,186),(703,186),(703,202)],CORAL)
        text(d,(1138,192),'Dado → campo',16,'#9B493D',anchor='ra')
    note(d,'Relação declarada entre dados e interface. O envio à API é outra operação.',y=553)

def milestone(d,year,name,meaning,detail=None):
    pill(d,426,187,'CONTEXTO HISTÓRICO',PALE,MUTED,13)
    text(d,(426,242),year,67,TEAL,True)
    d.line((627,247,627,455),fill=LINE,width=2)
    end=lines(d,(657,246),name,31,545,NAVY,True,41)
    lines(d,(658,end+22),meaning,24,527,INK,leading=34)
    if detail:note(d,detail,y=503)

def generations(d,phase=0):
    pair(d,('AngularJS','Família 1.x\nControllers, $scope e serviços.'),
         ('Angular','Família 2 em diante\nComposição por componentes e TypeScript.'),
         labels=('PRIMEIRA GERAÇÃO','A PARTIR DE 2016'))
    note(d,'2016: reescrita do framework. A migração exige planejamento.',y=529)

def exercise(d,which,answers=False):
    if which=='waiting':
        heading(d,'Pausa para pensar','Por que continua em “Enviando”?')
        request_form(d,'waiting')
        note(d,'O serviço informou uma falha, mas o indicador não parou.',y=548)
    elif which=='failure':
        heading(d,'Sua primeira análise de uma demanda','O que a interface deveria fazer?')
        cards(d,[('Informação','Qual informação apareceu antes da hora?'),
                 ('Espera','O que deveria aparecer durante o envio?'),
                 ('Falha','O que fazer com o texto que a pessoa escreveu?')])
    elif which=='return':
        heading(d,'Para praticar sozinho','De volta à lista')
        cards(d,[('Antes','A pessoa filtra os pedidos por status.'),
                 ('Navegação','Abre os detalhes e depois retorna.'),
                 ('Problema','O filtro selecionado desaparece.')])
        note(d,'Qual estado foi perdido? Como verificar o comportamento esperado?')

def route(d,detail=False):
    box(d,(426,188,1209,526),WHITE,18,LINE,2)
    box(d,(446,203,1188,246),PALE,8,PALE)
    text(d,(462,214),'/solicitacoes/1042' if detail else '/solicitacoes',20,NAVY)
    if detail:
        text(d,(451,277),'Detalhes · SOL-1042',26,NAVY,True)
        text(d,(451,328),'Acesso à impressora',23,INK)
        pill(d,451,372,'Em atendimento','#EAF4F3',TEAL,17)
        text(d,(451,457),'← Voltar à lista',21,TEAL,True)
    else:
        text(d,(451,274),'Solicitações',26,NAVY,True)
        for n,(code,label) in enumerate([('SOL-1042','Acesso à impressora'),('SOL-1043','Dúvida sobre o sistema')]):
            y=329+n*79;box(d,(449,y,1186,y+62),PALE,10,PALE)
            text(d,(465,y+18),code,18,TEAL,True);text(d,(609,y+17),label,21,INK)
    note(d,'Endereços diferentes podem apresentar partes diferentes da aplicação.')

def component_map(d,phase=0):
    box(d,(426,188,1209,526),WHITE,18,LINE,2)
    text(d,(449,207),'CENTRAL DE SOLICITAÇÕES · MAQUETE',14,NAVY,True)
    entries=[(447,253,754,497,'Formulário'),(777,253,1188,382,'Lista'),(797,407,1168,480,'Status')]
    for n,(x,y,xx,yy,label) in enumerate(entries):
        active=n==phase
        box(d,(x,y,xx,yy),'#EAF4F3' if active else PALE,12,TEAL if active else LINE,3 if active else 1)
        text(d,(x+17,y+14),label,22,TEAL if active else INK,True)
        if n==0:
            for k in range(3):box(d,(x+17,y+61+k*48,xx-17,y+91+k*48),WHITE,5,LINE)
        elif n==1:
            text(d,(x+18,y+65),'SOL-1042  ·  Acesso à impressora',17,MUTED)
        else:text(d,(x+135,y+18),'Em atendimento',18,MUTED)
    note(d,'Cada componente tem uma responsabilidade que podemos explicar.')

def security(d):
    pair(d,('Solicitante','Consulta os próprios pedidos.'),('Atendimento','Consulta a fila autorizada.'),
         labels=('PERFIL 01','PERFIL 02'),h=246)
    box(d,(426,461,1209,530),'#FFF0EA',14,'#FFF0EA')
    text(d,(449,478),'A API também precisa verificar a permissão.',24,'#93452F',True)

def crew(i):
    for end,team in [(7,['HELENA','LIA','PROF. RODRIGO']),
                     (14,['PROF. RODRIGO','DAVI','LIA']),
                     (31,['PROF. RODRIGO','LIA','CAIO']),
                     (37,['PROF. RODRIGO','BIA','RAFAEL']),
                     (44,['PROF. RODRIGO','CAIO']),
                     (60,['PROF. RODRIGO','CAIO','MARINA']),
                     (78,['PROF. RODRIGO','LIA']),
                     (86,['PROF. RODRIGO','MARINA']),
                     (94,['PROF. RODRIGO','CAIO']),
                     (102,['PROF. RODRIGO','BIA','RAFAEL']),
                     (110,['HELENA','PROF. RODRIGO','LIA','RAFAEL']),
                     (114,['PROF. RODRIGO','DAVI'])]:
        if i<=end:return team

@functools.lru_cache(24)
def panel(i,phase):
    if i<8:return v.pilot_panel(i,phase)
    item=v.DATA[i];im=v.base(item['speaker'],crew(i));d=ImageDraw.Draw(im)
    if i==8:
        heading(d,'Como vamos aprender','Os cards acompanham as entregas.');sol_card(d)
        note(d,'Entender, construir e conferir podem atravessar mais de uma aula.',y=447)
    elif i==9:
        heading(d,'Ao final da formação','Transformar demandas em soluções.')
        cards(d,[('Entender','Ler a demanda e esclarecer os critérios.'),('Implementar','Construir e integrar a solução em Angular.'),('Verificar','Investigar o resultado e conferir o comportamento.')])
    elif i in (10,11,12):
        heading(d,'A base continua presente','HTML, CSS e JavaScript')
        cards(d,[('HTML','Estrutura e significado do conteúdo.'),('CSS','Apresentação e organização visual.'),('JavaScript','Dados, eventos e comportamento.')])
        note(d,'Aqui: revisão aplicada. Os fundamentos terão uma formação própria.')
    elif i==13:
        heading(d,'Estude no seu ritmo','Pausar também faz parte.')
        cards(d,[('Pausar','Anote a dúvida e observe o exemplo.'),('Experimentar','Teste uma ideia quando chegarmos à prática.'),('Retomar','Volte ao trecho e compare o que aconteceu.')])
    elif i==14:
        heading(d,'Material e prática','Código de referência + sua solução')
        pair(d,('Referência da formação','github.com/codigoemtela'),('Seu repositório','Mantenha sua implementação e suas decisões.'),labels=('MATERIAL','PRÁTICA'))
        note(d,'Hoje: acompanhe os exemplos e anote suas respostas.')
    elif i==15:
        heading(d,'Antes do framework','O formulário já usa a base da web.');request_form(d)
        note(d,'HTML estrutura. CSS apresenta. JavaScript trata as interações.')
    elif i in (16,17,18):
        heading(d,'Separando as responsabilidades','Interface, API e persistência');api(d,False,i==18)
    elif i in (19,20,21):
        heading(d,'Estados do envio','A tela precisa representar a espera.')
        state='waiting' if i!=21 else ['waiting','success','error'][phase]
        request_form(d,state)
        note(d,'Estado do envio do formulário; o status do atendimento é outra informação.')
    elif i==22:
        heading(d,'Um conceito para o nosso raciocínio','O que chamamos de estado?')
        definition(d,'Estado','Informações que descrevem a situação da aplicação em um determinado momento.',
                   'Exemplos: filtro selecionado, pedido aberto e operação em andamento.')
    elif i in (23,24):
        heading(d,'Cada resultado precisa de tratamento','Sucesso e erro têm caminhos próprios.')
        pair(d,('Confirmação','Parar a espera, mostrar o protocolo e apresentar o resultado.'),
             ('Falha','Parar a espera, explicar a situação e preservar o texto.'),labels=('SUCESSO','ERRO'))
        note(d,'Ao tentar novamente, a mensagem anterior também precisa ser tratada.')
    elif i==25:exercise(d,'waiting')
    elif i==26:
        heading(d,'Uma hipótese para investigar','O caminho de erro também termina.')
        cards(d,[('Hipótese','O indicador foi atualizado apenas no sucesso.'),('Investigação','Compare o tratamento dos dois resultados.'),('Critério','O estado de espera deve terminar nos dois caminhos.')])
    elif i in (27,28,29):
        heading(d,'Uma alteração, mais de uma apresentação','Lista e detalhes precisam concordar.')
        status_sync(d,phase if i==27 else 1,i==28)
    elif i in (30,31):
        heading(d,'Atualizar a interface e receber novos dados','São responsabilidades diferentes.')
        pair(d,('Dentro da aplicação','Organizar como os dados recebidos aparecem nas partes da tela.'),
             ('Entre computadores','Usar um mecanismo de comunicação para buscar ou receber mudanças.'),labels=('INTERFACE','COMUNICAÇÃO'))
    elif i in (32,33):
        heading(d,'A pergunta da UX','Uma mensagem precisa orientar.')
        pair(d,('Erro','A pessoa não sabe se perdeu o texto ou o que pode fazer.'),
             ('Falha no envio','Seu texto foi preservado. Você pode tentar novamente.'),labels=('MENSAGEM VAGA','MENSAGEM COM ORIENTAÇÃO'))
        note(d,'Texto e próxima ação comunicam o resultado; a cor pode reforçar.')
    elif i==34:
        heading(d,'A pergunta do QA','Vamos verificar mais de um caminho.')
        cards(d,[('Dados válidos','A confirmação apresenta o protocolo.'),('Campo obrigatório','A mensagem identifica o que está faltando.'),('Serviço indisponível','A falha preserva o preenchimento.')])
    elif i in (35,36,37):
        heading(d,'Organização que ajuda a manter','Reaproveitar exige responsabilidade.')
        cards(d,[('Compartilhar','A mesma apresentação pode servir à lista e aos detalhes.'),('Entender','Partes parecidas podem ter comportamentos diferentes.'),('Manter','Defina limites que façam sentido para a demanda.')])
    elif i in (38,39):
        heading(d,'A história começa com outra geração','A origem do AngularJS')
        milestone(d,'2009','AngularJS','Interfaces dinâmicas e relações entre os dados e a apresentação.',
                  'Miško Hevery · desenvolvimento com Google e comunidade')
    elif i==40:
        heading(d,'Descrever a intenção da interface','Uma abordagem declarativa')
        pair(d,('Procurar e alterar','Procurar o elemento e trocar seu texto.'),('Expressar a relação','A prévia apresenta o título informado.'),labels=('DESCRIÇÃO EM PORTUGUÊS','DESCRIÇÃO EM PORTUGUÊS'))
        note(d,'São descrições de abordagem, e não exemplos de código executável.')
    elif i in (41,42,43,44):
        heading(d,'Dados relacionados à apresentação','Template e data binding')
        binding(d,phase if i==41 else 20,i in (43,44))
    elif i in (45,46):
        heading(d,'O que muda para a equipe','Uma relação que podemos encontrar.')
        pair(d,('Template','A prévia apresenta o título informado.'),('Dado mantido no código','A aplicação mantém o valor do título.'),labels=('APRESENTAÇÃO','INFORMAÇÃO'))
        note(d,'Explicitar a relação ajuda a entender a intenção da implementação.')
    elif i in (47,48):
        heading(d,'O comportamento continua sendo escrito','O framework participa da atualização.')
        cards(d,[('Enviar','Decidir quando a operação deve começar.'),('Interpretar','Tratar a resposta recebida.'),('Reagir','Definir os caminhos de confirmação e de falha.')])
    elif i in (49,50):
        heading(d,'Organizar responsabilidades e dependências','Serviços e injeção de dependências')
        definition(d,'Fornecer o que uma parte precisa','A dependência é fornecida conforme a configuração do programa.',
                   'Esses conceitos já estavam presentes no AngularJS.')
    elif i==51:
        heading(d,'Reconheça a geração do material','Pistas de um tutorial de AngularJS')
        cards(d,[('Família 1.x','O nome AngularJS identifica essa geração.'),('Controllers e $scope','Esses nomes são pistas do modelo antigo.'),('Contexto histórico','Nossa implementação usará a família Angular.')])
    elif i in (52,53,57,58):
        heading(d,'Uma mudança de geração','AngularJS e Angular');generations(d)
    elif i in (54,55,56):
        heading(d,'Uma migração também é trabalho de produto','A transição precisa ser planejada.')
        cards(d,[('Conhecer a base','Identificar APIs, organização e fluxos existentes.'),('Adaptar gradualmente','A migração pode combinar partes antigas e novas.'),('Verificar','Conferir os fluxos enquanto a aplicação evolui.')])
    elif i in (59,60):
        heading(d,'O suporte encerrado foi o do AngularJS','Um marco da primeira geração')
        milestone(d,'2021','Fim do suporte oficial ao AngularJS','Comunicado publicado em janeiro de 2022.',
                  'Esse marco não representa o fim do Angular moderno.')
    elif i in (61,62,63):
        heading(d,'A evolução depois da reescrita','O framework também muda por dentro.')
        milestone(d,'2020','Angular 9 · Ivy','Infraestrutura de compilação e execução usada por padrão.',
                  'Reconheça o propósito; o primeiro componente não exige estudar todos os detalhes internos.')
    elif i in (64,65,66):
        heading(d,'Organizando as dependências dos componentes','Componentes standalone')
        milestone(d,'2022','Uma composição mais direta','Angular 14: prévia.\nAngular 15: APIs estáveis.',
                  'Standalone ainda pode depender de componentes e serviços. NgModules aparece em bases existentes.')
    elif i in (67,68):
        heading(d,'Valor e relações reativas','Signals')
        milestone(d,'2023','Angular 16 · prévia de signals','Um valor pode participar de relações que reagem às mudanças.',
                  'O propósito se conecta à coerência entre dados e interface.')
    elif i==69:
        heading(d,'A experiência de escrever e aprender','Templates e documentação')
        milestone(d,'2023','Angular 17','Nova sintaxe de condições e repetições, inicialmente em prévia.',
                  'A nova documentação chegou em angular.dev.')
    elif i==70:
        heading(d,'A linha do tempo continua','Confira a versão do exemplo.')
        cards(d,[('Material da formação','Versões definidas quando prepararmos o ambiente.'),('Documentação','Consulte a documentação correspondente à versão.'),('Referências externas','Evite combinar instruções de momentos diferentes.')])
    elif i==71:
        heading(d,'Uma definição com contexto','Angular')
        definition(d,'Framework para aplicações web','Uma estrutura para organizar interface, dependências e comportamento.',
                   'Código aberto · equipe no Google · participação da comunidade')
    elif i in (72,73):
        heading(d,'O grau de organização oferecido','Biblioteca e framework')
        pair(d,('Biblioteca','Fornece recursos que você chama na estrutura que escolheu.'),
             ('Framework','Também estabelece convenções e participa da execução da aplicação.'),labels=('RECURSOS','RECURSOS + ORGANIZAÇÃO'))
    elif i==74:
        heading(d,'Partes com responsabilidade definida','Um componente pode ser reaproveitado.');status_sync(d,1)
        box(d,(426,532,1209,583),WHITE,0,WHITE);note(d,'O componente de status pode aparecer na lista e nos detalhes.',y=547)
    elif i in (75,76):
        heading(d,'O que existe em um componente','Apresentação, dados e comportamento')
        cards(d,[('Template · HTML','Descreve a apresentação e sua relação com os dados.'),('Estilos · CSS','Organizam a apresentação visual.'),('Código · TypeScript','Expressa os dados e os comportamentos.')])
    elif i in (77,78):
        heading(d,'Dividir pelo comportamento','Bons limites ajudam na manutenção.');component_map(d,phase)
    elif i in (79,80,81,82,83,84,85,86):
        heading(d,'Serviços e comunicação','Quem faz o quê na integração?');api(d,True,i in (83,84,86))
    elif i==88 and phase>=2:
        if phase==2:
            heading(d,'Recursos para formulários','Validação orienta o preenchimento.');request_form(d,'empty')
            note(d,'Uma mensagem identifica o campo obrigatório que está faltando.')
        else:
            heading(d,'Carregar partes do código sob demanda','Lazy loading')
            definition(d,'Código sob demanda','Carregar quando for necessário.')
    elif i in (87,88,89):
        heading(d,'Navegação dentro da aplicação','O roteador relaciona endereço e tela.');route(d,phase>0)
    elif i in (90,91):
        heading(d,'A estratégia depende do produto','Angular permite diferentes formas de renderizar.')
        cards(d,[('No navegador','A interface interativa apresenta as mudanças.'),('No servidor','A renderização pode ocorrer no servidor.'),('Páginas estáticas','Algumas páginas podem ser geradas antecipadamente.')])
    elif i==92:
        heading(d,'Ferramentas que apoiam o desenvolvimento','A base continua sendo JavaScript.')
        cards(d,[('VS Code','Ambiente para trabalhar no projeto.'),('TypeScript','Tipos e verificação de certas inconsistências.'),('Em execução','Dados externos ainda precisam ser validados.')])
    elif i in (93,94):
        heading(d,'Ferramentas e resultado observado','Conferir o comportamento da demanda')
        pair(d,('Durante o desenvolvimento','As ferramentas ajudam a encontrar inconsistências.'),
             ('Na aplicação funcionando','Verificamos o que acontece nos fluxos reais.'),labels=('APOIO','VERIFICAÇÃO'))
    elif i in (95,96,97,98):
        heading(d,'Segurança envolve a implementação inteira','Quem pode executar a operação?');security(d)
    elif i==99:
        heading(d,'A experiência precisa ser projetada','Organizar componentes é uma parte.')
        cards(d,[('Textos claros','Explique o resultado e a próxima ação.'),('Teclado','A navegação precisa funcionar sem depender do mouse.'),('Recuperação','Ajude quem não conseguiu concluir uma ação.')])
    elif i in (100,101,102):
        heading(d,'Escolher a ferramenta com critério','Relacione a decisão a um problema.')
        cards(d,[('Necessidade','Telas, estados, integrações e comportamento.'),('Manutenção','Duplicação, dependências e informação inconsistente.'),('Adequação','Avalie o tamanho e as interações de cada produto.')])
    elif i==103:
        heading(d,'Vamos retomar a demanda','Registrar e conseguir acompanhar');sol_card(d)
        note(d,'A seguir: avalie o comportamento da interface diante de uma falha.',y=446)
    elif i==104:
        if phase<3:
            heading(d,'Cenário com comportamento incorreto','Uma confirmação antes da hora')
            cards(d,[('A pessoa escreve','Preenche a descrição e clica em enviar.'),
                     ('A interface se antecipa','Limpa os campos e anuncia sucesso antes da resposta.'),
                     ('A resposta chega','A API informa que o registro falhou.')],phase+1)
        else:exercise(d,'failure')
    elif i in (105,106,107):
        heading(d,'Conferindo os caminhos','Os critérios vêm da necessidade.')
        cards(d,[('Durante a espera','Informar que o envio está em andamento.'),
                 ('Com a confirmação','Mostrar o protocolo recebido da API.'),
                 ('Diante da falha','Preservar o texto e terminar o indicador de envio.')])
    elif i==108:
        heading(d,'A entrega precisa ser confiável','O que a mensagem permite concluir?')
        definition(d,'Informar o que aconteceu','Uma mensagem de sucesso precisa corresponder ao resultado confirmado.',
                   'A pessoa deve conseguir confiar na informação apresentada.')
    elif i==109:exercise(d,'return')
    elif i==110:
        heading(d,'Explique com suas palavras','Duas perguntas para retomar a aula')
        pair(d,('Por que Angular?','Que necessidades deste projeto justificam a escolha?'),
             ('AngularJS ou Angular?','Que pistas ajudam a reconhecer a geração de um material?'),labels=('PROPOSTA','HISTÓRIA'))
        note(d,'Use os capítulos para voltar aos exemplos que ajudam sua explicação.')
    elif i==111:
        heading(d,'O card continua em A fazer','Critérios discutidos');sol_card(d)
        note(d,'A funcionalidade será implementada ao longo da formação.',y=444)
    elif i==112:
        heading(d,'O que construímos nesta primeira aula','Uma base para as próximas decisões')
        cards(d,[('Proposta','Organizar interfaces com várias interações.'),('História','AngularJS, a reescrita e a evolução do Angular.'),('Projeto','Componentes, estado e comunicação com a API.')])
    elif i==113:
        heading(d,'Na próxima aula','Como dados e interface se relacionam')
        component_map(d,phase)
        box(d,(426,532,1209,588),WHITE,0,WHITE)
        note(d,'Um componente pequeno. Uma ação. Um dado que muda na tela.',y=545)
    elif i==114:
        heading(d,'Conte sua dúvida com contexto','Vamos continuar a conversa.')
        cards(d,[('Localize','Anote o trecho da aula.'),('Descreva','Explique o que entendeu e onde surgiu a dúvida.'),('Compartilhe','Envie sua pergunta por mensagem.')])
    else:raise ValueError(f'Unmapped dialogue {i}')
    return im

def phase(i,local):
    if i<8:return v.phases(i,local)
    item=v.DATA[i];dur=item['duration']
    if i==21:return sum(local>=t for t in [v.key_time(item,'confirmação',3)+.2,v.key_time(item,'falha',9)-.3])
    if i==27:return int(local>=v.key_time(item,'confirma',6)+1.0)
    if i==41:return min(20,max(0,int((local-3)*5)))
    if i in (77,78,113):return min(2,int(max(0,local)/max(1,dur/3)))
    if i==88:return sum(local>=t for t in [dur*.18,v.key_time(item,'formulários',10)-.1,
                                          v.key_time(item,'lazy',dur-3)-.1])
    if i in (87,89):return int(local>=dur*.42)
    if i==104:
        return sum(local>=t for t in [v.key_time(item,'limpou',4)-.6,
                                      v.key_time(item,'falhou',10)-.4,
                                      v.key_time(item,'três',13)-.6])
    return 0
