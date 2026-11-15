const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
for(const n of process.argv.slice(2)){await p.goto('file://'+path.resolve(n+'.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
await p.screenshot({path:n+'.png'});
await p.addStyleTag({content:'body::after{content:"";position:fixed;inset:0;border-top:250px solid rgba(255,0,0,.25);border-bottom:400px solid rgba(255,0,0,.25);border-right:120px solid rgba(255,0,0,.25)}'});
await p.screenshot({path:n+'-safezone.png'});}
await b.close()})();
