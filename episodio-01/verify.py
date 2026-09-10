# SPDX-License-Identifier: GPL-3.0-only
"""Validate the delivered episode and export its actual first video frame."""
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parent
VIDEO=ROOT.parent/'Aula_01_Introducao_ao_Angular_Codigo_em_Tela.mp4'

def main():
    timeline=json.loads((ROOT/'timeline.json').read_text())
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams',
                                             '-show_chapters','-of','json',str(VIDEO)],text=True))
    video=next(x for x in info['streams'] if x['codec_type']=='video')
    audio=next(x for x in info['streams'] if x['codec_type']=='audio')
    assert video['codec_name']=='h264' and audio['codec_name']=='aac'
    assert (video['width'],video['height'])==(1280,720)
    assert abs(float(info['format']['duration'])-timeline['duration'])<.1
    assert len(info['chapters'])==8
    for actual,expected in zip(info['chapters'],timeline['chapters']):
        assert abs(float(actual['start_time'])-expected[0])<.01
    print('Metadados e oito capítulos conferidos.',flush=True)
    decoded=subprocess.run(['ffmpeg','-v','error','-i',str(VIDEO),'-f','null','-'],
                           capture_output=True,text=True)
    assert decoded.returncode==0 and not decoded.stderr.strip(),decoded.stderr
    print('Decodificação integral de vídeo e áudio sem erros.',flush=True)
    output=ROOT/'qa'/'thumbnail-frame-%02d.png'
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(VIDEO),'-vf',
                    'select=eq(n\\,0)+eq(n\\,119)','-fps_mode','vfr','-frames:v','2',str(output)],check=True)
    first=Image.open(ROOT/'qa/thumbnail-frame-01.png').convert('RGB')
    last=Image.open(ROOT/'qa/thumbnail-frame-02.png').convert('RGB')
    original=Image.open(ROOT/'assets/thumb-original.png').convert('RGB').resize((1280,720),Image.Resampling.LANCZOS)
    a,b,c=[np.asarray(x,dtype=float) for x in (first,last,original)]
    change=float(np.abs(a-b).mean());source_difference=float(np.abs(a-c).mean())
    assert change<3 and source_difference<5,(change,source_difference)
    target=ROOT.parent/'Thumb_Aula_01_Introducao_ao_Angular.png'
    temporary=target.with_name('Thumb_Aula_01_temporaria.png')
    first.save(temporary)
    with temporary.open('rb') as f:os.fsync(f.fileno())
    temporary.replace(target)
    report={
        'duration_seconds':float(info['format']['duration']),
        'resolution':[video['width'],video['height']],
        'fps':video['r_frame_rate'],'video_codec':video['codec_name'],'audio_codec':audio['codec_name'],
        'chapters':len(info['chapters']),'speech_blocks':len(timeline['scenes']),
        'spoken_words':sum(len(x['text'].split()) for x in timeline['scenes']),
        'caption_blocks':sum(len(x['captions']) for x in timeline['scenes']),
        'thumbnail_hold_seconds':5,
        'thumbnail_first_last_mean_pixel_difference':round(change,4),
        'thumbnail_source_mean_pixel_difference':round(source_difference,4),
        'complete_decode_errors':0,
        'video_bytes':VIDEO.stat().st_size,
        'video_sha256':hashlib.sha256(VIDEO.read_bytes()).hexdigest(),
        'approved_script_sha256':hashlib.sha256((ROOT/'roteiro-aprovado.md').read_bytes()).hexdigest(),
    }
    (ROOT/'verificacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)

if __name__=='__main__':main()
