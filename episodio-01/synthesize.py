# SPDX-License-Identifier: GPL-3.0-only
"""Generate all approved episode dialogue, with resumable atomic outputs."""
import asyncio
import hashlib
import json
import re
import shutil
from pathlib import Path

import edge_tts
import edge_tts.communicate
import edge_tts.voices

ROOT = Path(__file__).resolve().parent
for module in (edge_tts.communicate, edge_tts.voices):
    module._SSL_CTX.load_verify_locations('/etc/ssl/certs/ca-certificates.crt')

# Three Brazilian voice bases; stable prosody profiles distinguish the cast.
VOICE = {
    'HELENA': ('pt-BR-ThalitaMultilingualNeural','-8%','+0Hz'),
    'LIA': ('pt-BR-FranciscaNeural','-3%','+0Hz'),
    'PROF. RODRIGO': ('pt-BR-AntonioNeural','-10%','+0Hz'),
    'CAIO': ('pt-BR-AntonioNeural','+1%','+14Hz'),
    'RAFAEL': ('pt-BR-AntonioNeural','-5%','-15Hz'),
    'DAVI': ('pt-BR-AntonioNeural','-4%','+6Hz'),
    'BIA': ('pt-BR-FranciscaNeural','-1%','-13Hz'),
    'MARINA': ('pt-BR-ThalitaMultilingualNeural','-6%','-16Hz'),
}

def parse():
    chapter=section=''
    result=[]
    for line in (ROOT/'roteiro-aprovado.md').read_text().splitlines():
        if line.startswith('## '):chapter=line[3:];section=chapter
        if line.startswith('### '):section=line[4:]
        if line.startswith('@'):
            speaker,text=line[1:].split(': ',1)
            v,r,p=VOICE[speaker]
            i=len(result)
            result.append(dict(id=i,chapter=chapter,section=section,speaker=speaker,
                               text=text,voice=v,rate=r,pitch=p,audio=f'audio/{i:03d}.mp3'))
    return result

async def generate(item, semaphore):
    i=item['id'];stem=ROOT/'audio'/f'{i:03d}'
    if stem.with_suffix('.json').exists() and stem.with_suffix('.mp3').stat().st_size>1000:
        previous=json.loads(stem.with_suffix('.json').read_text())
        if all(previous.get(k)==item[k] for k in ['text','voice','rate','pitch']):
            return previous
    # Preserve the exact approved opening audio.
    pilot=ROOT.parent/'piloto-angular/audio'/f'{i:02d}'
    if i<8 and pilot.with_suffix('.json').exists():
        previous=json.loads(pilot.with_suffix('.json').read_text())
        assert previous['text']==item['text']
        shutil.copy2(pilot.with_suffix('.mp3'),stem.with_suffix('.mp3'))
        item['words']=previous['words']
        stem.with_suffix('.json').write_text(json.dumps(item,ensure_ascii=False,indent=2))
        return item
    async with semaphore:
        for attempt in range(3):
            try:
                words=[]
                async def stream():
                    c=edge_tts.Communicate(item['text'],voice=item['voice'],rate=item['rate'],
                                          pitch=item['pitch'],boundary='WordBoundary',
                                          connect_timeout=20,receive_timeout=60)
                    with stem.with_suffix('.part').open('wb') as out:
                        async for chunk in c.stream():
                            if chunk['type']=='audio':out.write(chunk['data'])
                            elif chunk['type']=='WordBoundary':
                                words.append(dict(text=chunk['text'],start=chunk['offset']/1e7,
                                                  duration=chunk['duration']/1e7))
                await asyncio.wait_for(stream(),120)
                assert words and stem.with_suffix('.part').stat().st_size>1000
                stem.with_suffix('.part').replace(stem.with_suffix('.mp3'))
                item['words']=words
                stem.with_suffix('.json').write_text(json.dumps(item,ensure_ascii=False,indent=2))
                print(f"OK {i:03d}/114 {item['speaker']} {len(words)} palavras",flush=True)
                return item
            except Exception as exc:
                print(f'RETRY {i:03d} {attempt+1}: {type(exc).__name__} {exc}',flush=True)
                if attempt==2:raise
                await asyncio.sleep(2)

async def main():
    items=parse()
    (ROOT/'dialogue.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))
    semaphore=asyncio.Semaphore(3)
    result=await asyncio.gather(*(generate(x,semaphore) for x in items))
    (ROOT/'narration.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(f'COMPLETE {len(result)} falas',flush=True)

if __name__=='__main__':asyncio.run(main())
