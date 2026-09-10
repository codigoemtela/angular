# SPDX-License-Identifier: GPL-3.0-only
"""Render the approved pilot: original vector screens + illustrated characters.

Requirements: Python 3.12, Pillow, NumPy, FFmpeg (with libx264).
Run: python render.py --stills   /   python render.py
"""
import bisect
import functools
import json
import math
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W, H, FPS, SR = 1280, 720, 24, 24000
NAVY = '#122746'
TEAL = '#157E83'
CORAL = '#DC715E'
INK = '#243951'
MUTED = '#647388'
LINE = '#DCE4EB'
PALE = '#F2F6F8'
WHITE = '#FFFFFF'
ACCENTS = {'HELENA': '#A13F57', 'LIA': TEAL, 'PROF. RODRIGO': '#365D91'}
NAMES = {'HELENA': 'Helena', 'LIA': 'Lia', 'PROF. RODRIGO': 'Prof. Rodrigo'}
ROLES = {'HELENA': 'PO · Product Owner', 'LIA': 'Começando no frontend', 'PROF. RODRIGO': 'Professor'}
ACCENTS.update({'CAIO':'#A07821','MARINA':'#B15B43','DAVI':'#547B57','RAFAEL':'#416A91','BIA':'#885887'})
NAMES.update({'CAIO':'Caio','MARINA':'Marina','DAVI':'Davi','RAFAEL':'Rafael','BIA':'Bia'})
ROLES.update({'CAIO':'Desenvolvedor JavaScript','MARINA':'Sistemas corporativos','DAVI':'SM · Scrum Master','RAFAEL':'QA · Qualidade de software','BIA':'UX · Experiência do usuário'})
COLS = {'HELENA': 0, 'LIA': 1, 'PROF. RODRIGO': 2}
FONTS = Path('/usr/share/fonts/truetype/dejavu')

@functools.lru_cache(None)
def font(size, bold=False):
    return ImageFont.truetype(str(FONTS / ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')), size)

def text(d, xy, value, size=24, color=INK, bold=False, anchor=None):
    d.text(xy, value, font=font(size, bold), fill=color, anchor=anchor)

def wrap(value, size, width, bold=False):
    result, current = [], ''
    for word in value.split():
        candidate = (current + ' ' + word).strip()
        if font(size, bold).getlength(candidate) > width and current:
            result.append(current)
            current = word
        else:
            current = candidate
    if current:
        result.append(current)
    return result

def lines(d, xy, value, size=24, width=720, color=INK, bold=False, leading=None):
    x, y = xy
    for line in wrap(value, size, width, bold):
        text(d, (x, y), line, size, color, bold)
        y += leading or round(size * 1.38)
    return y

def box(d, bounds, fill=WHITE, radius=18, outline=LINE, width=1):
    d.rounded_rectangle(bounds, radius, fill=fill, outline=outline, width=width)

def pill(d, x, y, label, fill=PALE, color=MUTED, size=15, border=None):
    width = round(font(size, True).getlength(label)) + 26
    box(d, (x, y, x+width, y+31), fill, 15, border or fill)
    text(d, (x+13, y+6), label, size, color, True)
    return width

def bubble_icon(d, x, y, color=TEAL, scale=1):
    d.rounded_rectangle((x, y, x+30*scale, y+22*scale), 5*scale, outline=color, width=2)
    d.line((x+6*scale, y+22*scale, x+6*scale, y+28*scale, x+13*scale, y+22*scale), fill=color, width=2)
    for n in range(3):
        d.ellipse((x+(6+8*n)*scale, y+9*scale, x+(8+8*n)*scale, y+11*scale), fill=color)

def check(d, x, y, color=TEAL, width=3):
    d.line((x, y+6, x+6, y+12, x+18, y), fill=color, width=width)

def base(speaker=None, team=None):
    im = Image.new('RGB', (W, H), WHITE)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 62), fill=NAVY)
    text(d, (32, 18), 'CÓDIGO EM TELA', 21, WHITE, True)
    text(d, (1248, 24), 'AULA 01  /  INTRODUÇÃO AO ANGULAR', 14, '#C1D0E0', anchor='ra')
    if speaker:
        accent = ACCENTS[speaker]
        d.line((391, 96, 391, 570), fill=LINE, width=1)
        text(d, (38, 105), NAMES[speaker], 28, NAVY, True)
        text(d, (39, 145), ROLES[speaker], 16, MUTED)
        d.rounded_rectangle((38, 178, 86, 182), 2, fill=accent)
        # The three names identify the team throughout the conversational cuts.
        x = 39
        if team is None:
            team = ['HELENA','LIA','PROF. RODRIGO'] if speaker in ['HELENA','LIA','PROF. RODRIGO'] else ['PROF. RODRIGO',speaker,'LIA']
        for other in team:
            label=NAMES[other].replace('Prof. ','')
            active = other == speaker
            pw = pill(d, x, 548, label,
                      '#E9EFF6' if active else WHITE,
                      accent if active else MUTED, 13,
                      '#D5DFEA' if active else LINE)
            x += pw + 7
    return im

def heading(d, eyebrow, title):
    text(d, (425, 97), eyebrow.upper(), 13, TEAL, True)
    size=31
    while font(size,True).getlength(title)>786:size-=1
    text(d, (425, 123), title, size, NAVY, True)

def section_card(d, x, y, label, description, number=None, color=TEAL, w=784, h=87):
    box(d, (x, y, x+w, y+h), PALE, 16, PALE)
    if number:
        box(d, (x+18, y+20, x+62, y+64), WHITE, 12, WHITE)
        text(d, (x+40, y+27), number, 23, color, True, 'ma')
    tx = x + (80 if number else 23)
    text(d, (tx, y+14), label, 22, NAVY, True)
    text(d, (tx, y+47), description, 17, MUTED)

def sol_card(d, x=426, y=189, w=783, compact=False):
    h = 121 if compact else 218
    box(d, (x, y, x+w, y+h), WHITE, 18, LINE, 2)
    text(d, (x+24, y+21), 'SOL 01', 16, TEAL, True)
    pill(d, x+w-109, y+15, 'A fazer', '#FFF0D5', '#76551F', 14)
    text(d, (x+24, y+60), 'Registrar uma solicitação', 26, NAVY, True)
    if not compact:
        lines(d, (x+24, y+108),
              'O colaborador registra um pedido e recebe um protocolo para acompanhá-lo.',
              22, w-58, MUTED)

def form(d, x=426, y=188, w=783, highlight=False):
    box(d, (x, y, x+w, y+338), WHITE, 18, LINE, 2)
    d.line((x, y+45, x+w, y+45), fill=LINE)
    text(d, (x+21, y+13), 'CENTRAL DE SOLICITAÇÕES', 14, NAVY, True)
    text(d, (x+w-19, y+14), 'MAQUETE', 12, MUTED, anchor='ra')
    text(d, (x+23, y+64), 'Título', 16, INK, True)
    box(d, (x+22, y+91, x+w-22, y+137), '#FAFCFD', 9)
    text(d, (x+36, y+102), 'Não consigo acessar o sistema', 18, MUTED)
    text(d, (x+23, y+154), 'Descrição', 16, INK, True)
    box(d, (x+22, y+181, x+w-22, y+256), '#FAFCFD', 9)
    text(d, (x+36, y+193), 'O acesso falha ao entrar na página inicial.', 18, MUTED)
    box(d, (x+22, y+277, x+253, y+320), TEAL, 10, TEAL)
    text(d, (x+39, y+287), 'Enviar solicitação', 19, WHITE, True)
    if highlight:
        d.rounded_rectangle((x+15, y+270, x+260, y+327), 15, outline=CORAL, width=3)

@functools.lru_cache(16)
def pilot_panel(i, phase):
    speaker = DATA[i]['speaker']
    im = base(speaker)
    d = ImageDraw.Draw(im)
    if i == 0:
        heading(d, 'O problema da equipe', 'Por onde chegam os pedidos?')
        info = [
            ('Mensagem', 'Não consigo acessar o sistema.'),
            ('E-mail', 'A impressora do setor parou.'),
            ('No corredor', 'Você viu meu pedido?'),
        ]
        for n, (label, desc) in enumerate(info):
            y = 188 + n*99
            if phase >= n+1:
                section_card(d, 426, y, label, desc, f'{n+1:02d}')
        if phase == 0:
            text(d, (429, 239), 'Pedir ajuda é só', 39, NAVY, True)
            text(d, (429, 294), 'o começo da conversa.', 39, NAVY, True)
            text(d, (431, 375), 'Depois, precisamos acompanhar o pedido.', 23, MUTED)
        if phase >= 4:
            box(d, (426, 500, 1209, 566), '#FFF0EA', 14, '#FFF0EA')
            text(d, (449, 517), 'Quem está cuidando disso?', 24, '#93452F', True)
    elif i == 1:
        heading(d, 'Uma dúvida bastante familiar', 'A tela principal da empresa…')
        box(d, (426, 188, 1209, 528), PALE, 20, PALE)
        bubble_icon(d, 453, 214, TEAL)
        text(d, (498, 211), 'Conversa da equipe', 22, NAVY, True)
        pill(d, 1009, 206, '150 mensagens', '#FFF0EA', '#93452F', 13)
        for n, (label, right) in enumerate([
            ('Alguém consegue me ajudar?', False),
            ('Quem pegou esse pedido?', True),
            ('Está lá em cima na conversa…', False),
        ]):
            x = 470 if not right else 719
            y = 275+n*70
            fill = WHITE if not right else '#DDEFEF'
            box(d, (x, y, x+445, y+54), fill, 15, fill)
            text(d, (x+18, y+16), label, 18, INK)
        text(d, (427, 548), 'A informação existe. Encontrá-la dá trabalho.', 19, MUTED)
    elif i == 2:
        heading(d, 'O que precisamos melhorar', 'Um lugar para acompanhar.')
        for n, (a,b) in enumerate([
            ('Registrar', 'Um ponto de entrada para os pedidos.'),
            ('Acompanhar', 'O colaborador consegue ver o andamento.'),
            ('Organizar a fila', 'A equipe assume os pedidos e informa o status.'),
        ]):
            if phase >= n:
                section_card(d, 426, 188+n*112, a, b, f'{n+1:02d}', h=96)
    elif i == 3:
        heading(d, 'O projeto da formação', 'Central de solicitações internas')
        sol_card(d)
        if phase >= 1:
            text(d, (426, 442), 'DA NECESSIDADE À FUNCIONALIDADE', 14, MUTED, True)
            labels = ['Entender', 'Construir', 'Conferir']
            for n, label in enumerate(labels):
                x = 426+n*268
                box(d, (x, 477, x+246, 541), '#EAF4F3', 14, '#EAF4F3')
                text(d, (x+123, 495), label, 23, TEAL, True, 'ma')
    elif i == 4:
        heading(d, 'A primeira pergunta da Lia', 'É só criar os campos e salvar?')
        form(d, highlight=phase >= 1)
        pill(d, 426, 544, 'SOL 01  ·  A fazer', '#FFF0D5', '#76551F', 13)
    elif i == 5:
        heading(d, 'Antes de implementar', 'O formulário pede decisões.')
        prompts = [
            ('Espera', 'Se a resposta demorar, o que aparece?'),
            ('Falha', 'Se o registro falhar, o texto desaparece?'),
            ('Acesso', 'Quem pode consultar esse pedido depois?'),
        ]
        for n, (a,b) in enumerate(prompts):
            if phase >= n:
                section_card(d, 426, 188+n*111, a, b, '?', h=97)
        pill(d, 426, 540, 'SOL 01  ·  A fazer', '#FFF0D5', '#76551F', 13)
    elif i == 6:
        heading(d, 'Como conferir a entrega', 'O colaborador precisa saber.')
        box(d, (426, 188, 1209, 431), '#EAF4F3', 20, '#EAF4F3')
        text(d, (452, 208), 'EXEMPLO DE CONFIRMAÇÃO', 13, TEAL, True)
        d.ellipse((452, 247, 491, 286), fill=TEAL)
        check(d, 462, 258, WHITE, 3)
        text(d, (507, 250), 'Solicitação registrada', 26, NAVY, True)
        text(d, (452, 309), 'Protocolo', 16, MUTED)
        text(d, (452, 340), 'SOL-0001', 32, TEAL, True)
        text(d, (452, 392), 'Use o protocolo para acompanhar o pedido.', 18, INK)
        text(d, (426, 456), 'Confirmação clara + um jeito de encontrar depois.', 22, NAVY, True)
        pill(d, 426, 511, 'SOL 01  ·  A fazer', '#FFF0D5', '#76551F', 13)
    elif i == 7:
        heading(d, 'O assunto da nossa primeira aula', 'Onde o Angular entra?')
        box(d, (426, 189, 1209, 420), NAVY, 20, NAVY)
        text(d, (454, 211), 'Angular', 54, WHITE, True)
        text(d, (457, 284), 'Framework de desenvolvimento web', 23, '#D5E3F0')
        lines(d, (457, 329), 'Recursos e convenções para construir e organizar aplicações.',
              23, 691, WHITE)
        if phase >= 1:
            pill(d, 426, 445, 'O que se propõe a resolver', '#EAF4F3', TEAL, 17)
        if phase >= 2:
            pill(d, 426, 490, 'Como chegou até aqui', '#EAF4F3', TEAL, 17)
        if phase >= 3:
            text(d, (427, 552), 'Depois, voltamos ao card para analisar uma situação.', 18, MUTED)
    return im

def key_time(item, phrase, fallback):
    # Word-level timing is returned by the voice service. Use original spelling.
    needle = phrase.lower()
    for w in item['words']:
        if w['text'].lower().strip('.,!?;:') == needle:
            return w['start']
    return fallback

def phases(i, local):
    item = DATA[i]
    if i == 0:
        ts = [key_time(item,'mensagem',8), key_time(item,'e-mail',9),
              key_time(item,'corredor',11), key_time(item,'quem',13)]
        return sum(local >= t-.2 for t in ts)
    if i == 2:
        return int(local >= key_time(item,'acompanhar',7)-.3) + int(local >= key_time(item,'fila',10)-.4)
    if i == 3:
        return int(local > 12)
    if i == 4:
        return int(local > 2.8)
    if i == 5:
        return int(local >= key_time(item,'falhar',8)-1.2) + int(local >= key_time(item,'consultar',12)-1)
    if i == 7:
        return (int(local >= key_time(item,'primeira',13)-1) +
                int(local >= key_time(item,'chegou',18)-.3) +
                int(local >= key_time(item,'final',22)-.3))
    return 0
