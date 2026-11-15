# Usage: python3 -I make_vo.py <naskah.json> <version> <model.onnx> <out.wav>
import json,subprocess,sys,os,tempfile
naskah,ver,model,out=sys.argv[1:5]
segs=json.load(open(naskah))[ver]
tmp=tempfile.mkdtemp()
def dur(f):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode())
inputs=[];report=[]
for i,(t0,t1,text) in enumerate(segs):
    win=t1-t0-0.15;ls=1.15
    while True:
        f=f'{tmp}/s{i}.wav'
        subprocess.run(['piper','-m',model,'--length-scale',str(ls),'--sentence-silence','0.3','-f',f],input=text.encode(),check=True,capture_output=True)
        d=dur(f)
        if d<=win or ls<=0.95: break
        ls=round(ls-0.05,2)
    report.append((i,t0,round(d,2),round(win,2),ls,'OK' if d<=win else 'TOO LONG'))
    inputs.append((f,t0))
for r in report:print(r)
args=['ffmpeg','-y','-v','error']
for f,_ in inputs:args+=['-i',f]
fc=''.join(f'[{i}:a]adelay={int(t*1000)}|{int(t*1000)}[a{i}];' for i,(_,t) in enumerate(inputs))
fc+=''.join(f'[a{i}]' for i in range(len(inputs)))+f'amix=inputs={len(inputs)}:normalize=0,highpass=f=90,lowpass=f=7200,aecho=0.85:0.5:45:0.12,loudnorm=I=-16:TP=-1.5:LRA=7[out]'
args+=['-filter_complex',fc,'-map','[out]','-ar','48000','-ac','2',out]
subprocess.run(args,check=True)
