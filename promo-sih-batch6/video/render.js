// Usage: node render.js preview t1 t2 ...   |   node render.js video out.mp4 [fps]
const {chromium}=require('playwright');const path=require('path');const {spawn}=require('child_process');
(async()=>{const [mode,...rest]=process.argv.slice(2);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
await p.goto('file://'+path.resolve('video.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
if(mode==='preview'){for(const t of rest){await p.evaluate(t=>seek(+t),t);await p.screenshot({path:`preview-${t}.png`});}}
else{const out=rest[0]||'out.mp4',fps=+(rest[1]||30);const D=await p.evaluate(()=>DURATION);const N=Math.round(D*fps);
 const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',String(fps),'-c:v','mjpeg','-i','-','-f','lavfi','-t',String(D),'-i','anullsrc=r=48000:cl=stereo','-shortest','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-r',String(fps),'-c:a','aac','-b:a','128k','-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
 for(let i=0;i<N;i++){await p.evaluate(t=>seek(t),i/fps);const buf=await p.screenshot({type:'jpeg',quality:92});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(i%300===0)console.log('frame',i,'/',N);}
 ff.stdin.end();await new Promise(r=>ff.on('close',r));}
await b.close();})();
