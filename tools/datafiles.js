// Round-trip codec for data.js / data-vault.js / data-senses.js / data-extra.js.
// node datafiles.js extract WEBDIR OUTDIR   -> data.json (without vault), vault.json (decoded rows), senses.json
// node datafiles.js build   INDIR WEBDIR VERSION -> rewrite the data files
// T3: studio.examples + pack live in data-extra.js (lazy chunk, loaded on demand by app.js)
const fs=require('fs'),vm=require('vm'),path=require('path');
const [cmd,a,b,ver]=process.argv.slice(2);
function load(dir){const ctx={window:{}};vm.createContext(ctx);for(const f of['data.js','data-vault.js','data-senses.js','data-extra.js']){if(fs.existsSync(path.join(dir,f)))vm.runInContext(fs.readFileSync(path.join(dir,f),'utf8'),ctx)}return ctx.window;}
const COLS=['id','set','kind','label','section','prompt','context','options','answer','explanation','tip','topic','diff'];
const STR=new Set(['id','kind','label','section','prompt','context','explanation','tip','topic']);
if(cmd==='extract'){
  const W=load(a);const D=W.__TGAT1_DATA;const [S,R]=D.vault;const g=i=>typeof i==='number'?S[i]:i;
  // verify which columns are string-indexed
  const rows=R.map(r=>{const o={};COLS.forEach((c,i)=>{o[c]=c==='options'?r[i].map(g):STR.has(c)?g(r[i]):r[i]});return o});
  const d=Object.assign({},D);delete d.vault;
  // T3: merge the lazy extra chunk back into data.json so the round-trip is lossless
  if(W.__TGAT1_DATA_EXTRA){
    if(W.__TGAT1_DATA_EXTRA.examples&&d.studio)d.studio.examples=W.__TGAT1_DATA_EXTRA.examples;
    if(W.__TGAT1_DATA_EXTRA.pack!==undefined)d.pack=W.__TGAT1_DATA_EXTRA.pack;
  }
  fs.mkdirSync(b,{recursive:true});
  fs.writeFileSync(path.join(b,'data.json'),JSON.stringify(d,null,1));
  fs.writeFileSync(path.join(b,'vault.json'),JSON.stringify(rows,null,1));
  fs.writeFileSync(path.join(b,'senses.json'),JSON.stringify(W.__TGAT1_SENSES,null,1));
  console.log('extracted',rows.length,'vault rows');
}else if(cmd==='build'){
  const d=JSON.parse(fs.readFileSync(path.join(a,'data.json')));const rows=JSON.parse(fs.readFileSync(path.join(a,'vault.json')));const sen=JSON.parse(fs.readFileSync(path.join(a,'senses.json')));
  const S=[],idx=new Map();const s=x=>{if(!idx.has(x)){idx.set(x,S.length);S.push(x)}return idx.get(x)};
  const R=rows.map(o=>COLS.map(c=>c==='options'?o.options.map(s):STR.has(c)?s(o[c]):o[c]));
  const hdr=`/* TGAT1 English Studio v${ver} — core vocabulary and learning content. */\n`;
  // T3: studio.examples + pack go to the lazy data-extra.js chunk
  const extra={};
  if(d.studio&&d.studio.examples){extra.examples=d.studio.examples;delete d.studio.examples}
  if(d.pack!==undefined){extra.pack=d.pack;delete d.pack}
  fs.writeFileSync(path.join(b,'data.js'),hdr+'window.__TGAT1_DATA='+JSON.stringify(d)+';\n');
  if(Object.keys(extra).length){
    fs.writeFileSync(path.join(b,'data-extra.js'),`/* TGAT1 English Studio v${ver} — lazy chunk: legacy example mirror + pack content. Loaded on demand by app.js (TGAT1_ensureExtra). */\nwindow.__TGAT1_DATA_EXTRA=`+JSON.stringify(extra)+';\n');
  }
  fs.writeFileSync(path.join(b,'data-vault.js'),`/* TGAT1 English Studio v${ver} — question bank (Long Conversation, Text Completion and Reading revised in rounds 2–3). */\nwindow.__TGAT1_DATA=window.__TGAT1_DATA||{};\nwindow.__TGAT1_DATA.vault=`+JSON.stringify([S,R])+';\n');
  fs.writeFileSync(path.join(b,'data-senses.js'),'window.__TGAT1_SENSES='+JSON.stringify(sen)+';\n');
  console.log('built',R.length,'rows',S.length,'strings');
}
