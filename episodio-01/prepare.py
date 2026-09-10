# SPDX-License-Identifier: GPL-3.0-only
"""Validate speech, align captions and build the exact audio/video timeline."""
import concurrent.futures
import hashlib
import json
import math
import re
import subprocess
import time
import wave
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parent
SR=24000
FPS=24
CHAPTER_TITLES={
 1:'O pedido que precisa virar uma aplicação',
 2:'Como vamos aprender nesta formação',
 3:'O que fica difícil quando a interface cresce',
 4:'A história do Angular e as mudanças de geração',
 5:'Como o Angular ajuda a organizar nossa central',
 6:'O que continua sendo responsabilidade da equipe',
 7:'Sua primeira análise de uma demanda',
 8:'Fechamento e próxima aula',
}

def norm(s):return ''.join(c.casefold() for c in s if c.isalnum())

def align_words(item):
    raw=item['text'].split();spoken=item['words']
    a=''.join(norm(w) for w in raw);b=''.join(norm(w['text']) for w in spoken)
    assert a==b, f"Speech metadata differs from approved text at {item['id']}: {a} / {b}"
    spans=[];p=0
    for w in spoken:
        n=len(norm(w['text']))
        if n:spans.append((p,p+n,w));p+=n
    result=[];cursor=0
    def locate(pos,end=False):
        for lo,hi,w in spans:
            if lo<=pos<hi or (end and lo<pos<=hi):
                return w['start']+w['duration']*(pos-lo)/(hi-lo)
        return spoken[-1]['start']+spoken[-1]['duration']
    for token in raw:
        n=len(norm(token));start=locate(cursor);end=locate(cursor+n,True)
        result.append(dict(text=token,start=start,duration=max(.01,end-start)))
        cursor+=n
    return result

def captions(item):
    words=align_words(item);groups=[];current=[]
    for j,w in enumerate(words):
        current.append(w)
        line=' '.join(x['text'] for x in current)
        next_len=len(line)+(len(words[j+1]['text'])+1 if j+1<len(words) else 0)
        if w['text'][-1:] in '.?!' or next_len>88 or j==len(words)-1:
            groups.append(dict(text=line,start=current[0]['start'],
                               end=w['start']+w['duration']+.16))
            current=[]
    for j in range(len(groups)-1):groups[j]['end']=min(groups[j]['end'],groups[j+1]['start'])
    assert ' '.join(x['text'] for x in groups)==item['text']
    return groups

def normalize(original):
    i=original['id'];stem=ROOT/'audio'/f'{i:03d}'
    limit=time.monotonic()+420
    while not stem.with_suffix('.json').exists():
        if time.monotonic()>limit:raise RuntimeError(f'Audio {i} not ready')
        time.sleep(2)
    item=json.loads(stem.with_suffix('.json').read_text())
    assert item['text']==original['text']
    target=stem.with_name(stem.name+'-mix.wav')
    valid=False
    if target.exists():
        with wave.open(str(target),'rb') as w:
            n=w.getnframes();actual=len(w.readframes(n))//2
            valid=n==actual and actual/SR>=item['words'][-1]['start']+item['words'][-1]['duration']-.12
    if not valid:
        temp=stem.with_name(stem.name+'-temp.wav')
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(stem.with_suffix('.mp3')),
                        '-af','loudnorm=I=-18:TP=-2:LRA=11','-ar',str(SR),'-ac','1',str(temp)],check=True)
        temp.replace(target)
    with wave.open(str(target),'rb') as w:
        n=w.getnframes();audio=np.frombuffer(w.readframes(n),dtype=np.int16).copy()
        assert len(audio)==n
    item['duration']=len(audio)/SR
    assert item['duration']>=item['words'][-1]['start']+item['words'][-1]['duration']-.12
    item['captions']=captions(item)
    stride=SR//FPS
    item['energy']=[round(float(np.sqrt(np.mean(audio[k:k+stride].astype(float)**2)))/6000,3)
                    for k in range(0,len(audio),stride)]
    print(f'Preparado {i:03d} {item["duration"]:.1f}s',flush=True)
    return item,audio

def main():
    originals=json.loads((ROOT/'dialogue.json').read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        normalized=list(pool.map(normalize,originals))
    events=[];audio_parts=[];cursor=0;chapter_marks=[]
    def add(kind,duration,payload=None,audio=None):
        nonlocal cursor
        frames=math.ceil((duration-1e-9)*FPS)
        seconds=frames/FPS
        event=dict(kind=kind,start=cursor/FPS,end=(cursor+frames)/FPS,frames=frames)
        event.update(payload or {})
        events.append(event)
        target=frames*(SR//FPS)
        if audio is None:audio=np.zeros(target,dtype=np.int16)
        elif len(audio)<target:audio=np.pad(audio,(0,target-len(audio)))
        audio_parts.append(audio[:target])
        cursor+=frames
        return event
    def ident(seconds):
        a=np.zeros(round(seconds*SR),dtype=float)
        for delay,freq in [(.2,329.63),(.55,392),(.9,493.88),(1.25,659.25)]:
            t=np.arange(round(1.8*SR))/SR
            env=(1-np.exp(-t*55))*np.exp(-t*3.4)
            note=(np.sin(2*np.pi*freq*t)+.16*np.sin(4*np.pi*freq*t))*env*1000
            k=round(delay*SR);a[k:k+len(note)]+=note
        return a.astype(np.int16)
    # Requirement: exact same thumbnail image throughout the first five seconds.
    add('thumbnail',5,audio=ident(5))
    chapter_marks.append((0,1,CHAPTER_TITLES[1]))
    previous_chapter=1
    for j,(item,audio) in enumerate(normalized):
        chapter=int(item['chapter'][:2])
        if chapter!=previous_chapter:
            chapter_marks.append((cursor/FPS,chapter,CHAPTER_TITLES[chapter]))
            add('chapter',3.5,dict(chapter=chapter,title=CHAPTER_TITLES[chapter]))
            previous_chapter=chapter
        gap=.36 if j+1<len(normalized) and normalized[j+1][0]['speaker']==item['speaker'] else .62
        event=add('speech',item['duration']+gap,dict(id=j,chapter=chapter),audio)
        item['start']=event['start'];item['end']=event['end']
        if j==7:add('ident',4,audio=ident(4))
        if j==24:add('pause',8,dict(exercise='waiting',chapter=chapter))
        if j==104:add('pause',12,dict(exercise='failure',chapter=chapter))
    add('ending',4,audio=ident(4))
    full=np.concatenate(audio_parts)
    with wave.open(str(ROOT/'mix.wav'),'wb') as out:
        out.setparams((1,2,SR,len(full),'NONE','not compressed'));out.writeframes(full.tobytes())
    timeline=dict(duration=cursor/FPS,fps=FPS,events=events,chapters=chapter_marks,
                  scenes=[x[0] for x in normalized])
    (ROOT/'timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2))
    def stamp(t,srt=False):
        ms=round(t*1000)
        if srt:return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
        return f'{int(t)//60:02d}:{int(t)%60:02d}'
    cues=[]
    for item,_ in normalized:
        for c in item['captions']:cues.append((item['start']+c['start'],item['start']+c['end'],c['text']))
    srt='\n\n'.join(f'{j+1}\n{stamp(a,True)} --> {stamp(b,True)}\n{t}' for j,(a,b,t) in enumerate(cues))+'\n'
    (ROOT/'Aula_01_Introducao_ao_Angular.srt').write_text(srt)
    chapters='\n'.join(f'{stamp(t)} {title}' for t,c,title in chapter_marks)+'\n'
    (ROOT/'capitulos.txt').write_text(chapters)
    metadata=[';FFMETADATA1','title=Introdução ao Angular | Código em Tela | Aula 01']
    for k,(t,c,title) in enumerate(chapter_marks):
        end=chapter_marks[k+1][0] if k+1<len(chapter_marks) else cursor/FPS
        metadata+=['[CHAPTER]','TIMEBASE=1/1000',f'START={round(t*1000)}',f'END={round(end*1000)}',f'title={title}']
    (ROOT/'chapters.ffmeta').write_text('\n'.join(metadata)+'\n')
    print(json.dumps(dict(duration=cursor/FPS,chapters=chapters,dialogues=len(normalized),
                          words=sum(len(i['text'].split()) for i,_ in normalized)),ensure_ascii=False),flush=True)

if __name__=='__main__':main()
