const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();
const html='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>body{margin:0}</style></head><body>'+fs.readFileSync('3f4-lab-workbook.html','utf8')+'</body></html>';
fs.writeFileSync('full.html',html);
for(const [name,w,dark] of [['desk',1280,false],['mob',400,true]]){
 const p=await b.newPage({viewport:{width:w,height:900},colorScheme:dark?'dark':'light'});
 const errs=[];p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file://'+process.cwd()+'/full.html');await p.waitForTimeout(1500);
 const sw=await p.evaluate(()=>document.documentElement.scrollWidth);
 console.log(name,'scrollWidth',sw,'errors',errs);
 await p.screenshot({path:name+'.png',fullPage:true});
}
await b.close();})();
