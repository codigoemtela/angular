# SPDX-License-Identifier: GPL-3.0-only
"""Render the full episode from its approved speech and exact visual timeline."""
import argparse
import bisect
import functools
import json
import math
import os
import subprocess
from pathlib import Path

from PIL import Image,ImageDraw
import visuals as v
import panels as p

ROOT=Path(__file__).resolve().parent
TIMELINE=json.loads((ROOT/'timeline.json').read_text())
DATA=TIMELINE['scenes'];EVENTS=TIMELINE['events'];FPS=24
DURATION=TIMELINE['duration'];W,H=1280,720
v.DATA=DATA
STARTS=[e['start'] for e in EVENTS]
THUMB=Image.open(ROOT/'assets/thumb-original.png').convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
SHEETS={key:Image.open(ROOT/'assets'/name).convert('RGB') for key,name in {
    'a':'helena-lia-rodrigo.png','b':'caio-marina-davi.png','c':'rafael-bia.png'}.items()}
RANGES={
 'HELENA':('a',[(0,0,515,508),(0,515,519,1015)]),
 'LIA':('a',[(524,0,974,508),(526,515,973,1015)]),
 'PROF. RODRIGO':('a',[(987,0,1536,508),(985,515,1536,1015)]),
 'CAIO':('b',[(0,0,550,511),(0,515,550,1024)]),
 'MARINA':('b',[(550,0,1022,511),(550,515,1022,1024)]),
 'DAVI':('b',[(1024,0,1536,511),(1024,515,1536,1024)]),
 'RAFAEL':('c',[(0,0,688,640),(0,650,688,1254)]),
 'BIA':('c',[(697,0,1254,640),(697,650,1254,1254)]),
}

@functools.lru_cache(32)
def portrait(speaker,pose):
    key,rectangles=RANGES[speaker]
    tile=SHEETS[key].crop(rectangles[pose])
    ratio=min(354/tile.width,354/tile.height)
    tile=tile.resize((round(tile.width*ratio),round(tile.height*ratio)),Image.Resampling.LANCZOS)
    canvas=Image.new('RGB',(354,354),v.WHITE)
    canvas.paste(tile,((354-tile.width)//2,354-tile.height))
    return canvas

@functools.lru_cache(700)
def caption_lines(value):
    rows=v.wrap(value,26,1150)
    assert len(rows)<=2,(value,rows)
    if len(rows)==2:
        words=value.split()
        candidates=[]
        for n in range(1,len(words)):
            a,b=' '.join(words[:n]),' '.join(words[n:])
            aw,bw=v.font(26).getlength(a),v.font(26).getlength(b)
            if max(aw,bw)<=1150:candidates.append((abs(aw-bw),[a,b]))
        if candidates:rows=min(candidates,key=lambda x:x[0])[1]
    return rows

def subtitles(im,speaker,caption,t,chapter):
    d=ImageDraw.Draw(im)
    d.rectangle((0,608,W,H),fill=v.NAVY)
    accent=v.ACCENTS.get(speaker,v.TEAL)
    d.rectangle((0,608,W,611),fill=accent)
    v.text(d,(32,620),v.NAMES.get(speaker,speaker).upper(),12,'#AFC7D9',True)
    v.text(d,(1248,620),f'CAPÍTULO {chapter:02d} / 08',12,'#AFC7D9',anchor='ra')
    if caption:
        rows=caption_lines(caption);y=644 if len(rows)==2 else 657
        for row in rows:
            v.text(d,(640,y),row,26,v.WHITE,anchor='ma');y+=33
    d.rectangle((0,716,round(W*t/DURATION),719),fill='#58B3B3')
    return im

@functools.lru_cache(12)
def chapter_card(chapter,title):
    im=Image.new('RGB',(W,H),v.NAVY);d=ImageDraw.Draw(im)
    v.text(d,(77,84),'CÓDIGO EM TELA',23,'#A4C9CA',True)
    v.pill(d,78,172,f'CAPÍTULO {chapter:02d}','#243D5C','#DFE9F2',16)
    v.lines(d,(74,258),title,49,1020,v.WHITE,True,leading=69)
    d.rounded_rectangle((79,539,168,545),3,fill=v.CORAL)
    v.text(d,(79,579),'Aula 01 · Introdução ao Angular',24,'#B8CDD9')
    for n in range(8):
        x=80+n*144;d.rounded_rectangle((x,651,x+125,656),2,fill=v.TEAL if n<chapter else '#30455F')
    return im

@functools.lru_cache(2)
def ident_card(ending=False):
    im=Image.new('RGB',(W,H),v.NAVY);d=ImageDraw.Draw(im)
    v.text(d,(82,84),'CÓDIGO EM TELA',25,'#A4C9CA',True)
    v.text(d,(82,194),'Na próxima aula' if ending else 'Introdução ao Angular',44,v.WHITE,True)
    title='Como um componente relaciona dados e interface' if ending else 'Uma demanda. Uma equipe. Uma aplicação.'
    v.lines(d,(83,285),title,36,880,v.WHITE,True,leading=50)
    d.rounded_rectangle((84,449,174,455),3,fill=v.CORAL)
    v.text(d,(83,516),'youtube.com/@codigoemtela',26,'#E0EAF2',True)
    v.text(d,(83,563),'github.com/codigoemtela',24,'#A4C9CA')
    v.text(d,(84,652),'FORMAÇÃO ANGULAR · AULA 01',16,'#A4C9CA',True)
    return im

def raw_frame(t):
    idx=min(len(EVENTS)-1,max(0,bisect.bisect_right(STARTS,t)-1));event=EVENTS[idx]
    kind=event['kind'];local=max(0,t-event['start'])
    if kind=='thumbnail':return THUMB.copy()
    if kind=='chapter':return chapter_card(event['chapter'],event['title']).copy()
    if kind in ('ident','ending'):return ident_card(kind=='ending').copy()
    if kind=='pause':
        speaker='LIA' if event['exercise']=='waiting' else 'PROF. RODRIGO'
        im=v.base(speaker,p.crew(25 if event['exercise']=='waiting' else 104));d=ImageDraw.Draw(im);p.exercise(d,event['exercise'])
        im.paste(portrait(speaker,0),(27,187))
        d=ImageDraw.Draw(im)
        d.rectangle((28,539,382,595),fill=v.WHITE)
        remaining=max(1,math.ceil(event['end']-t))
        v.pill(d,40,550,f'{remaining}s para pensar','#FFF0D5','#76551F',15)
        return subtitles(im,'PAUSA PARA PENSAR','Pause para anotar sua resposta.',t,event['chapter'])
    item=DATA[event['id']];i=item['id'];phase=p.phase(i,local)
    im=p.panel(i,phase).copy()
    before=p.phase(i,local-.3)
    if phase!=before:
        lo,hi=local-.3,local
        for _ in range(10):
            mid=(lo+hi)/2
            if p.phase(i,mid)==phase:hi=mid
            else:lo=mid
        a=max(0,min(1,(local-hi)/.3));a=a*a*(3-2*a)
        im=Image.blend(p.panel(i,before),im,a)
    speaking=.08<=local<item['duration']-.2
    dy=round(2*math.sin(local*1.8)) if speaking else 0
    im.paste(portrait(item['speaker'],1 if speaking else 0),(27,187+dy))
    d=ImageDraw.Draw(im)
    energy=item['energy'][min(len(item['energy'])-1,round(local*FPS))] if speaking else 0
    for n in range(8):
        h=3+min(12,round(energy*9*(.5+.5*math.sin(t*16+n*.9))))
        x=103+n*8;d.rounded_rectangle((x,180-h//2,x+3,180+h//2),1,fill=v.ACCENTS[item['speaker']])
    cap=next((c['text'] for c in item['captions'] if c['start']-.04<=local<c['end']),'')
    return subtitles(im,item['speaker'],cap,t,event['chapter'])

def frame(t):
    idx=min(len(EVENTS)-1,max(0,bisect.bisect_right(STARTS,t)-1));event=EVENTS[idx]
    current=raw_frame(t)
    # No fade-in: frame zero is the thumbnail, held unchanged for exactly 120 frames.
    if event['kind']=='thumbnail':return current
    start=event['start']
    if 0<=t-start<.22:
        previous=raw_frame(max(0,start-.001))
        return Image.blend(previous,current,(t-start)/.22)
    if t>DURATION-.5:
        return Image.blend(current,Image.new('RGB',(W,H),v.NAVY),min(1,(t-DURATION+.5)/.5))
    return current

def qa():
    directory=ROOT/'qa';directory.mkdir(exist_ok=True)
    for item in DATA:
        for c in item['captions']:caption_lines(c['text'])
    shots=[]
    # Check each dialogue at a representative point, plus every important visual state.
    moments=[(f'd{i:03d}',x['start']+min(x['duration']*.55,13)) for i,x in enumerate(DATA)]
    moments += [(f'variation-{i}-{n}',DATA[i]['start']+delta)
                for i,values in {0:[1,10,20],21:[2,12],27:[1,13],41:[4,9,21],77:[1,9,17],
                                 104:[2,7,12,20]}.items() for n,delta in enumerate(values)
                if delta<DATA[i]['duration']]
    moments += [('thumbnail',0),('ident',EVENTS[9]['start']+1)]
    moments += [(f'pause-{e["exercise"]}',e['start']+2) for e in EVENTS if e['kind']=='pause']
    moments += [(f'chapter-{e["chapter"]}',e['start']+1) for e in EVENTS if e['kind']=='chapter']
    moments += [('ending',DURATION-2)]
    for name,t in moments:
        im=frame(t);im.save(directory/f'{name}.png');shots.append((name,im))
    for k in range(0,len(shots),12):
        sheet=Image.new('RGB',(1280,6*383),v.WHITE);d=ImageDraw.Draw(sheet)
        for j,(name,im) in enumerate(shots[k:k+12]):
            x,y=j%2*640,j//2*383
            sheet.paste(im.resize((640,360),Image.Resampling.LANCZOS),(x,y))
            v.text(d,(x+9,y+360),name,15,v.NAVY,True)
        sheet.save(directory/f'contact-{k//12:02d}.jpg',quality=87)
    assert frame(0).tobytes()==frame(119/FPS).tobytes(), 'First five seconds must match thumbnail'
    print(json.dumps(dict(duration=DURATION,frames=round(DURATION*FPS),qa_images=len(shots),
                          captions=sum(len(x['captions']) for x in DATA)),indent=2),flush=True)

def render():
    output=ROOT.parent/'Aula_01_Introducao_ao_Angular_Codigo_em_Tela.mp4'
    temporary=ROOT/'video-em-producao.mp4'
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','warning','-thread_queue_size','64',
         '-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}',
         '-r',str(FPS),'-i','-','-i',str(ROOT/'mix.wav'),'-i',str(ROOT/'chapters.ffmeta'),
         '-map','0:v:0','-map','1:a:0','-map_metadata','2','-map_chapters','2',
         '-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p',
         '-c:a','aac','-b:a','128k','-ar','48000','-movflags','+faststart','-shortest',
         '-metadata','comment=Roteiro aprovado, personagens e vozes sintéticos; telas didáticas simuladas.',str(temporary)]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    count=round(DURATION*FPS)
    for n in range(count):
        process.stdin.write(frame(n/FPS).tobytes())
        if n%(FPS*30)==0:
            print(f'Render {n/FPS:7.1f}/{DURATION:.1f}s ({n/count*100:.1f}%)',flush=True)
    process.stdin.close()
    if process.wait()!=0:raise RuntimeError('Video encoding failed')
    with temporary.open('rb') as ready:os.fsync(ready.fileno())
    temporary.replace(output)
    print(f'COMPLETE {output}',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--qa',action='store_true');args=parser.parse_args()
    qa() if args.qa else render()
