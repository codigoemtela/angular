# Código em Tela — Aula 01: Introdução ao Angular

Canal: https://www.youtube.com/@codigoemtela  
GitHub do projeto: https://github.com/codigoemtela

Episódio completo produzido a partir do roteiro aprovado por Rodrigo Brito e
do padrão audiovisual do piloto aprovado. Duração: **33min15s**.

## Conteúdo da entrega

- 115 falas, preservando as 3.883 palavras do roteiro aprovado.
- Os oito personagens: professor Rodrigo, Helena, Lia, Caio, Marina, Davi,
  Rafael e Bia.
- O primeiro quadro contém a thumbnail. A mesma imagem permanece fixa
  durante **5 segundos**, antes da abertura com Helena.
- Oito capítulos, 434 blocos de legendas e duas pausas para pensar, de 8 e
  12 segundos. As soluções só aparecem depois das pausas.
- História do AngularJS e do Angular, exemplos de estados da interface,
  componentes, API, navegação, permissões e análise de uma demanda.
- Animação simples com poses, pequenos movimentos, transições e elementos
  didáticos. Não é animação labial por fonema.
- Telas desenhadas por código como maquetes didáticas. Não são capturas de
  uma implementação pronta da central.
- Exportação em 1280 × 720, 24 fps, H.264/AAC, com capítulos no MP4.

O card **SOL 01** permanece em **A fazer**. A discussão dos critérios não é
apresentada como entrega da funcionalidade. Os protocolos exibidos são
exemplos fictícios.

## Organização dos arquivos

- `roteiro-aprovado.md`: roteiro integral com as fontes técnicas e históricas.
- `publicacao-youtube.txt`: título, descrição e capítulos para publicação.
- `capitulos.txt`: marcações temporais do vídeo final.
- `Aula_01_Introducao_ao_Angular.srt`: legendas externas, além das legendas
  já desenhadas no vídeo.
- `assets/`: thumbnail original e folhas de poses dos personagens.
- `audio/000.mp3` a `audio/114.mp3`: falas em arquivos independentes.
- `audio/*.json`: texto e marcações temporais retornadas pela síntese.
- `dialogue.json` e `narration.json`: elenco e sequência das falas.
- `timeline.json`: montagem completa, incluindo capítulos e pausas.
- `synthesize.py`: geração das falas.
- `prepare.py`: alinhamento das legendas, normalização e montagem do áudio.
- `visuals.py`, `panels.py` e `render.py`: desenho das cenas e exportação.
- `verificacao.json`: verificações técnicas do arquivo entregue.

O MP4 e a thumbnail extraída de seu primeiro quadro são entregues
separadamente, para facilitar o uso e evitar duplicá-los neste pacote.

## Perfis de voz

Foram usadas três vozes-base em português brasileiro, com ajustes estáveis
de ritmo e altura para os oito personagens. Os áudios da abertura são os
mesmos aprovados no piloto.

| Personagem | Voz-base | Ritmo | Altura |
|---|---|---|---|
| Professor Rodrigo | pt-BR-AntonioNeural | −10% | 0 Hz |
| Helena | pt-BR-ThalitaMultilingualNeural | −8% | 0 Hz |
| Lia | pt-BR-FranciscaNeural | −3% | 0 Hz |
| Caio | pt-BR-AntonioNeural | +1% | +14 Hz |
| Rafael | pt-BR-AntonioNeural | −5% | −15 Hz |
| Davi | pt-BR-AntonioNeural | −4% | +6 Hz |
| Bia | pt-BR-FranciscaNeural | −1% | −13 Hz |
| Marina | pt-BR-ThalitaMultilingualNeural | −6% | −16 Hz |

A síntese foi feita sem cobrança ou chave de API com
[edge-tts](https://github.com/rany2/edge-tts), que utiliza o serviço online de
leitura do Microsoft Edge. A geração futura depende da disponibilidade e
das condições do serviço. Nenhuma voz de pessoa real foi clonada.

As pequenas vinhetas musicais foram criadas por síntese de notas, sem usar
uma gravação musical externa. A narração não tem música de fundo.

## Reproduzir a produção

Ambiente usado: Linux, Python 3.12, Pillow, NumPy, FFmpeg com libx264 e
DejaVu Sans em `/usr/share/fonts/truetype/dejavu`.

Para montar o vídeo usando os áudios incluídos:

```bash
python -m pip install pillow numpy
python prepare.py
python render.py --qa
python render.py
```

Execute na pasta que contém os scripts. O MP4 é salvo na pasta
imediatamente superior. A opção `--qa` produz quadros de revisão em `qa/`.

Para refazer as vozes, com acesso ao serviço online:

```bash
python -m pip install edge-tts==7.2.8
python synthesize.py
```

Se mudar o texto ou o perfil de uma voz, remova o respectivo arquivo
`audio/NNN-mix.wav` antes de preparar o áudio novamente. Os scripts de síntese
mantêm a verificação TLS e usam também as autoridades de certificação do
sistema Linux. As instruções acima descrevem a produção audiovisual; o
ambiente das aulas práticas da formação será apresentado separadamente.

## Licenças e créditos

Código original deste pacote: **GPL-3.0-only**. Texto integral em `LICENSE`.

Roteiro, ilustrações e materiais originais: **CC BY 4.0**, conforme a decisão
do projeto. Atribuição sugerida: “Código em Tela — Rodrigo Brito”, com link
para https://github.com/codigoemtela e indicação das alterações realizadas.
Licença: https://creativecommons.org/licenses/by/4.0/

Componentes de terceiros e serviços de voz conservam suas próprias
licenças e condições. A licença do código deste pacote não altera essas
condições. As fontes do conteúdo estão preservadas no roteiro.
