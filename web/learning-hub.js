/* TGAT1 English Studio v42.0.0 — Learning Hub (guided 70-unit path).
   Additive layer loaded after app.js. It does not replace any page and never locks the rest of
   the app. It reuses: the 1,200-question bank (VLT_BANK), existing statistics (VLT_record),
   the unified error notebook (STUDIO_RECORD_ERROR), Grammar Clinic, Reading Lab, vocabulary
   games, the Everyday-English drill and the 20 full mock sets. Its own state lives in one
   localStorage key with a versioned schema. Curriculum content: learning-hub-curriculum.js. */
(function(){
'use strict';
if(window.TGAT1Hub)return;
const W=window,D=document;
const KEY='tgat1_learning_hub_v1',SCHEMA=1,UNITS=70,DAY=86400000;
const PASS_PCT=80;
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const now=()=>Date.now();
const today=()=>{const d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')};
const clamp=(n,a,b)=>Math.max(a,Math.min(b,n));
const isObj=x=>!!x&&typeof x==='object'&&!Array.isArray(x);
function shuffle(a){a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function toast(m){try{(W.studioToast||W.VLT_toast||function(){})(m)}catch(_){}}
function page(){try{return typeof STUDIO_PAGE!=='undefined'?STUDIO_PAGE:''}catch(_){return ''}}
function bankReady(){try{return typeof VLT_BANK!=='undefined'&&VLT_BANK.length>0}catch(_){return false}}
function ensureBank(){return typeof W.VLT_ensureBank==='function'?W.VLT_ensureBank():Promise.resolve([])}

/* ------------------------------------------------------------------ state + migration */
let HS=null,READONLY=false,NOTICE='';
function fresh(){return {schema:SCHEMA,createdAt:now(),updatedAt:now(),unit:1,units:{},active:null,pending:null,returnTo:false,
  concepts:{},errors:{},seen:{},history:[],assessments:[],reviewDay:'',stats:{answered:0,correct:0}}}
/* Versioned migrations. Schema 0 = any Learning Hub object without a `schema` field (for example a
   partially edited or hand-imported object). Each step must return a schema+1 object. */
const MIGRATIONS={
  0:function(s){const o=fresh();o.createdAt=Number(s.createdAt)||o.createdAt;
    o.unit=Number(s.currentUnit||s.unit)||1;
    const src=isObj(s.units)?s.units:(isObj(s.progress)?s.progress:{});
    for(const [k,v] of Object.entries(src))if(isObj(v))o.units[k]={st:(v.st==='done'||v.completed)?'done':'active',done:isObj(v.done)?v.done:(isObj(v.steps)?v.steps:{}),res:isObj(v.res)?v.res:{},att:Array.isArray(v.att)?v.att:(Array.isArray(v.attempts)?v.attempts:[])};
    ['concepts','errors','seen'].forEach(f=>{if(isObj(s[f]))o[f]=s[f]});
    ['history','assessments'].forEach(f=>{if(Array.isArray(s[f]))o[f]=s[f]});
    o.schema=1;return o;}
};
function normUnit(v){return {st:v.st==='done'?'done':'active',done:isObj(v.done)?v.done:{},res:isObj(v.res)?v.res:{},
  att:Array.isArray(v.att)?v.att.filter(isObj).slice(-20):[],remed:isObj(v.remed)?v.remed:null,
  started:Number(v.started)||0,completed:Number(v.completed)||0,used:Array.isArray(v.used)?v.used.map(String).slice(-200):[]}}
function normalize(s){
  const o=fresh();
  o.createdAt=Number(s.createdAt)||o.createdAt;o.updatedAt=Number(s.updatedAt)||0;
  if(isObj(s.units))for(const [k,v] of Object.entries(s.units)){const n=Number(k);if(Number.isInteger(n)&&n>=1&&n<=UNITS&&isObj(v))o.units[n]=normUnit(v)}
  // Sequential invariant: the current unit is the first unit that is not completed.
  let first=1;while(first<=UNITS&&o.units[first]&&o.units[first].st==='done')first++;
  o.unit=Math.min(first,UNITS);
  if(isObj(s.active)&&Array.isArray(s.active.items)&&s.active.items.length&&Number.isInteger(s.active.i)){
    const a=s.active;if(a.unit<=o.unit||a.mode==='review'||a.mode==='extra')o.active={...a,ans:Array.isArray(a.ans)?a.ans:[],i:clamp(a.i,0,a.items.length-1)};
  }
  if(isObj(s.pending)&&Number(s.pending.u)>=1&&Number(s.pending.u)<=o.unit)o.pending=s.pending;
  o.returnTo=!!s.returnTo;
  ['concepts','errors','seen'].forEach(f=>{if(isObj(s[f]))o[f]=s[f]});
  if(Array.isArray(s.history))o.history=s.history.filter(isObj).slice(-400);
  if(Array.isArray(s.assessments))o.assessments=s.assessments.filter(isObj).slice(-300);
  o.reviewDay=typeof s.reviewDay==='string'?s.reviewDay:'';
  if(isObj(s.stats))o.stats={answered:Number(s.stats.answered)||0,correct:Number(s.stats.correct)||0};
  // caps
  const errs=Object.entries(o.errors);if(errs.length>1500){errs.sort((a,b)=>(b[1].last||0)-(a[1].last||0));o.errors=Object.fromEntries(errs.slice(0,1500))}
  const seen=Object.entries(o.seen);if(seen.length>4000){seen.sort((a,b)=>(b[1].t||0)-(a[1].t||0));o.seen=Object.fromEntries(seen.slice(0,4000))}
  return o;
}
function backupRaw(tag,str){try{const k=KEY+'__backup_'+tag;if(localStorage.getItem(k)==null)localStorage.setItem(k,str)}catch(_){}}
function load(){
  let str=null;READONLY=false;NOTICE='';
  try{str=localStorage.getItem(KEY)}catch(e){READONLY=true;NOTICE='เบราว์เซอร์ไม่อนุญาตให้บันทึกข้อมูล ความคืบหน้าใน Learning Hub จะไม่ถูกเก็บ';return fresh()}
  if(str==null)return fresh();
  let raw;try{raw=JSON.parse(str)}catch(e){raw=undefined}
  if(!isObj(raw)){backupRaw('unreadable',str);NOTICE='ข้อมูล Learning Hub เดิมอ่านไม่ได้ ระบบเก็บสำเนาไว้ในเครื่องและเริ่มใหม่เฉพาะ Learning Hub (ข้อมูลส่วนอื่นไม่ถูกแตะต้อง)';return fresh()}
  const v=Number.isInteger(raw.schema)?raw.schema:0;
  if(v>SCHEMA){READONLY=true;NOTICE='ข้อมูล Learning Hub มาจากแอปเวอร์ชันที่ใหม่กว่า จึงเปิดแบบอ่านอย่างเดียวเพื่อไม่ให้ข้อมูลเสียหาย';return normalize(raw)}
  let s=raw;
  if(v<SCHEMA){backupRaw('schema'+v,str);for(let k=v;k<SCHEMA;k++){if(typeof MIGRATIONS[k]!=='function'){READONLY=true;NOTICE='ไม่พบขั้นตอนย้ายข้อมูล Learning Hub';return fresh()}s=MIGRATIONS[k](s)}}
  const out=normalize(s);
  if(v<SCHEMA){HS=out;save()}
  return out;
}
function save(){if(READONLY||!HS)return false;HS.updatedAt=now();try{localStorage.setItem(KEY,JSON.stringify(HS));return true}catch(e){toast('บันทึก Learning Hub ไม่สำเร็จ: พื้นที่จัดเก็บเต็ม');return false}}
function st(){if(!HS)HS=load();return HS}
function unitState(n){const s=st();if(!s.units[n])s.units[n]=normUnit({});return s.units[n]}
function log(e){const s=st();s.history.push({t:now(),...e});if(s.history.length>400)s.history.splice(0,s.history.length-400)}

/* ------------------------------------------------------------------ curriculum + items */
let IDX=null;
function cur(){return W.TGAT1_HUB_CURRICULUM||null}
function idx(){
  const c=cur();if(!c)return null;
  if(IDX&&IDX.c===c)return IDX;
  const items=new Map(),byC=new Map();
  (c.items||[]).forEach(r=>{const it={id:r[0],c:r[1],d:r[2]||2,stem:r[3],ctx:r[4]||'',opts:r[5],ans:r[6],hint:r[7]||'',why:r[8]||'',wrong:r[9]||[],src:'hub'};
    items.set(it.id,it);if(!byC.has(it.c))byC.set(it.c,[]);byC.get(it.c).push(it.id)});
  IDX={c,units:new Map(c.units.map(u=>[u.n,u])),items,byC,concepts:c.concepts||{},bankByC:null};
  return IDX;
}
function unitDef(n){const x=idx();return x?x.units.get(n):null}
function conceptDef(c){const x=idx();return (x&&x.concepts[c])||{t:c,skill:'mixed'}}

// Bank classification: each bank question gets one "family" used by curriculum concepts.
const TC_RULES=[
 ['tc.conditional',/conditional|\bUnless\b/i],['tc.participle',/participle|participial|reduced/i],['tc.passive',/passive/i],
 ['tc.relative',/relative|^(who|which|where|whose|that) ใช้|^(who|which|where|whose|that) เป็น/i],['tc.compare',/comparative|superlative|as \+ adjective \+ as|เปรียบเทียบ/i],
 ['tc.structure',/make it|too \+|make \+ object|suggest that|be advised|say ตามด้วย|ever more|so \+ adjective/i],
 ['tc.agreement',/เอกพจน์|พหูพจน์|เติม -s|every \+/i],
 ['tc.tense',/present perfect|past simple|past perfect|present continuous|present simple|future|tense|had \+ V3|be \+ V-ing|ปัจจุบัน|อดีต/i],
 ['tc.gerund-inf',/gerund|infinitive|หลัง hope|recommend|V-ing/i],['tc.collocation',/collocation/i],
 ['tc.modal',/cannot|could|must|should|modal/i],
 ['tc.connector',/เชื่อม|\bbecause\b|although|however|therefore|Fortunately|\band\b|\bafter\b|\bbut\b/i],
 ['tc.preposition',/preposition|\bat ใช้|ใช้ on|ใช้ in|\bwithout\b/i],
 ['tc.article-quant',/determiner|article|\ban\b|enough|quantifier|hundreds of|\bonly\b|\bany\b/i],
 ['tc.word-form',/adjective|adverb|noun|คำนาม|กริยา/i]];
function rcType(p){p=String(p||'');
  if(/main idea|mainly about|central|main point|summar|overall|chiefly|primarily discussing|as a whole|central focus/i.test(p))return'rc.main';
  if(/first|initial|begin|opened|sequence/i.test(p))return'rc.sequence';
  if(/reason|why|led the group|purpose/i.test(p))return'rc.reason';
  if(/mean|definition|understood|closest/i.test(p))return'rc.vocab';
  if(/infer|conclusion|supported|interpretation|suggest/i.test(p))return'rc.inference';
  if(/refer/i.test(p))return'rc.reference';
  return'rc.detail'}
function family(q){
  const c=q.category,p=String(q.prompt||'');
  if(c==='qr'){if(/^Q: (What time|How often|How long)/i.test(p))return'qr.time';if(/^Q: (Could you|Would you)/i.test(p))return'qr.request';
    if(/^Q: (Why don.t|What should|How about|Shall)/i.test(p))return'qr.suggest';if(/^Q: (I.m sorry|Thank|Sorry|Congrat)/i.test(p))return'qr.social';return'qr.opinion'}
  if(c==='short')return'conv.short';if(c==='long')return'conv.long';
  if(c==='rc')return rcType(p);
  if(c==='tc'){const e=String(q.explanation||'');for(const [k,re] of TC_RULES)if(re.test(e))return k;return'tc.other'}
  return'other'}
function bankPool(c){
  const x=idx();if(!x||!bankReady())return [];
  if(!x.bankByC)x.bankByC=new Map();
  if(x.bankByC.has(c))return x.bankByC.get(c);
  const def=x.concepts[c]||{};const fams=Array.isArray(def.bank)?def.bank:[];const re=def.bre?new RegExp(def.bre,'i'):null;
  const ids=fams.length?VLT_BANK.filter(q=>fams.includes(family(q))&&(!re||re.test(String(q.explanation||'')+' '+String(q.prompt||'')))).map(q=>q.id):[];
  x.bankByC.set(c,ids);return ids;
}
function bankItem(id){
  const q=typeof W.VLT_get==='function'?W.VLT_get(id):null;if(!q)return null;
  let why=q.explanation||'';try{if(typeof W.VLT_learningExplanation==='function')why=W.VLT_learningExplanation(q)||why}catch(_){}
  return {id:q.id,c:'',d:Number(q.difficulty)||2,stem:q.prompt,ctx:q.context||'',opts:q.options,ans:q.answer,hint:q.hint||'',why,wrong:null,src:'bank',fam:family(q),q};
}
function getItem(ref){if(!ref)return null;if(ref.src==='bank')return bankItem(ref.id);const x=idx();return x?x.items.get(ref.id)||null:null}
function conceptPool(c,src){
  const x=idx();if(!x)return [];
  const out=[];if(src!=='bank')(x.byC.get(c)||[]).forEach(id=>out.push({id,src:'hub',c}));
  if(src!=='hub')bankPool(c).forEach(id=>out.push({id,src:'bank',c}));
  return out;
}
function itemDifficulty(ref){const it=getItem(ref);return it?it.d:2}
// Choose n items for concept c, preferring unseen items, then least recently seen, closest difficulty.
function pick(c,n,opt={}){
  const s=st(),ex=opt.exclude||new Set(),d=opt.d||2;
  const pool=conceptPool(c,opt.src).filter(r=>!ex.has(r.id));
  const scored=pool.map(r=>{const sn=s.seen[r.id];const age=sn?now()-sn.t:1e13;const dd=Math.abs(itemDifficulty(r)-d);
    return {r,k:(sn?1:0)*1e6+(sn?Math.max(0,1e5-age/1000/60):0)+dd*1000+Math.random()*10}});
  scored.sort((a,b)=>a.k-b.k);
  return scored.slice(0,n).map(x=>x.r);
}

/* ------------------------------------------------------------------ mastery, error memory, review */
const IV=[1,3,7,14,30,60];
function cRec(c){const s=st();if(!isObj(s.concepts[c]))s.concepts[c]={a:0,k:0,r:[],st:'new',p:0,due:0,iv:0,du:0,last:0,mis:0,low:0,days:[],u:0};return s.concepts[c]}
function evalConcept(c){
  const r=cRec(c),last=r.r.slice(-5),avg=last.length?last.reduce((a,b)=>a+b,0)/last.length:0;
  const recentMis=r.recentMis&&now()-r.recentMis<14*DAY;
  if(r.a>=5&&last.length>=5&&avg>=0.8&&(r.days||[]).length>=2&&!recentMis){if(r.st!=='mastered'){r.st='mastered';r.p=0;r.iv=Math.max(r.iv,7);r.due=now()+r.iv*DAY}}
  else if(r.st==='mastered'&&r.r.slice(-2).every(v=>v===0)){r.st='learning';r.iv=1;r.due=now()+DAY}
  else if(r.st==='new')r.st='learning';
  return r;
}
/* Record one answer as evidence. conf: 'sure'|'some'|'not'|null. kind: 'first'|'hinted' */
function evidence(c,ok,conf,kind){
  const s=st(),r=cRec(c),t=now(),d=today();
  if(!r.u)r.u=s.unit;
  if(kind==='hinted'){r.last=t;return r}
  r.a++;if(ok)r.k++;
  let v=ok?1:0;
  if(ok&&conf==='not'){v=0.5;r.low++;r.p=clamp(r.p+1,0,20);r.due=Math.min(r.due||Infinity,t+DAY)}
  if(!ok){r.p=clamp(r.p+(conf==='sure'?3:2),0,20);r.iv=1;r.due=t+DAY;r.du=s.unit+2;if(conf==='sure'){r.mis++;r.recentMis=t}}
  r.r.push(v);if(r.r.length>12)r.r.splice(0,r.r.length-12);
  if(!(r.days||[]).includes(d)){r.days=(r.days||[]).concat(d).slice(-6)}
  r.last=t;
  s.stats.answered++;if(ok)s.stats.correct++;
  return evalConcept(c);
}
function scheduleAfterReview(c,ok){const r=cRec(c);if(ok){const i=Math.max(0,IV.indexOf(r.iv));r.iv=IV[Math.min(IV.length-1,(r.iv?i+1:0))];r.due=now()+r.iv*DAY;r.du=st().unit+Math.max(2,Math.round(r.iv/2));r.p=Math.max(0,r.p-2)}}
function errorType(ok,conf,c){if(ok)return conf==='not'?'guess':'';const r=cRec(c);if(conf==='sure')return'misconception';if(conf==='not')return'knowledge-gap';if(r.st==='mastered')return'slip';return'error'}
function remember(ref,item,sel,ok,conf,mode){
  const s=st();s.seen[ref.id]={n:((s.seen[ref.id]||{}).n||0)+1,t:now()};
  const c=ref.c||item.c||'';const def=conceptDef(c);
  const type=errorType(ok,conf,c);
  const e=s.errors[ref.id];
  if(!ok||e||type==='guess'){
    const row=e||{qid:ref.id,src:ref.src,c,skill:def.skill||'',att:0,wrong:0,recent:[],first:now()};
    row.att++;if(!ok)row.wrong++;row.recent=(row.recent||[]).concat(ok?1:0).slice(-6);
    row.type=type||row.type||'';row.sel=item.opts[sel]??'';row.ans=item.opts[item.ans]??'';
    row.why=String(item.why||'').slice(0,600);row.conf=conf||row.conf||null;row.last=now();row.mode=mode;row.unit=s.unit;
    const cr=cRec(c);row.st=cr.st;row.p=cr.p;row.due=cr.due;
    if(type==='guess'&&!e)row.wrong=0;
    s.errors[ref.id]=row;
  }
  // existing systems: statistics for bank questions + the unified error notebook
  try{if(ref.src==='bank'&&item.q&&typeof W.VLT_record==='function'&&mode!=='extra')W.VLT_record(item.q,ok)}catch(_){}
  try{if(typeof W.STUDIO_RECORD_ERROR==='function')W.STUDIO_RECORD_ERROR({id:(ref.src==='hub'?'hub-':'')+ref.id,module:'learning-hub',topic:def.t||c,prompt:item.stem,context:item.ctx||'',selected:item.opts[sel],answer:item.opts[item.ans],correct:ok,explanation:String(item.why||'').slice(0,600),at:now()})}catch(_){}
}
function dueConcepts(){
  const s=st(),t=now();
  return Object.entries(s.concepts).filter(([c,r])=>isObj(r)&&r.a>0&&(r.u||0)<s.unit&&((r.due&&r.due<=t)||(r.du&&s.unit>=r.du))&&!(r.st==='mastered'&&r.due>t))
    .sort((a,b)=>(b[1].p-a[1].p)||((a[1].due||0)-(b[1].due||0))).map(([c])=>c);
}

/* ------------------------------------------------------------------ unit steps */
const STEP_LABEL={learn:'เรียนแนวคิด',guided:'ฝึกพร้อมคำใบ้',practice:'ฝึกด้วยตนเอง',assess:'แบบทดสอบท้ายหน่วย'};
const ACT_LABEL={vlt:'ฝึกในศูนย์สอบ',mock:'ข้อสอบจำลองเต็มชุด',grammar:'Grammar Clinic',readingPlus:'Reading Lab',vocab:'เกมคำศัพท์',phrase:'Everyday English'};
function steps(u){
  const out=[{k:'learn',label:STEP_LABEL.learn}];
  if(u.guided)out.push({k:'guided',label:STEP_LABEL.guided});
  (u.act||[]).forEach((a,i)=>out.push({k:'act'+i,label:a.label||ACT_LABEL[a.type]||'กิจกรรม',act:a}));
  if(u.practice)out.push({k:'practice',label:STEP_LABEL.practice});
  out.push({k:'assess',label:STEP_LABEL.assess});
  return out;
}
function unitProgress(n){const u=unitDef(n),us=st().units[n];if(!u)return {done:0,total:0};const sp=steps(u);return {done:sp.filter(x=>us&&us.done[x.k]).length,total:sp.length}}
function locked(n){return n>st().unit}

/* ------------------------------------------------------------------ Continue Learning */
function nextAction(){
  const s=st();
  if(READONLY)return {k:'readonly'};
  if(s.active)return {k:'resume',run:s.active};
  if(s.pending){const res=verifyPending();if(!res)return {k:'external',p:s.pending}}
  const n=s.unit,u=unitDef(n);if(!u)return {k:'nocurriculum'};
  const us=unitState(n);
  if(us.st==='done'&&n===UNITS)return {k:'finished'};
  if(us.remed&&us.remed.required)return {k:'remed',u:n};
  const sp=steps(u),firstOpen=sp.find(x=>!us.done[x.k]);
  if(n>=3&&s.reviewDay!==today()&&firstOpen&&firstOpen.k!=='assess'&&dueConcepts().length>=2)return {k:'review'};
  if(!firstOpen)return {k:'complete-unit',u:n};
  return {k:'step',u:n,step:firstOpen};
}
function describe(a){
  const s=st();
  switch(a.k){
    case 'resume':{const r=a.run;return `ทำต่อ: ${runTitle(r)} · ข้อ ${r.i+1}/${r.items.length}`}
    case 'external':return `กลับไปทำกิจกรรมให้จบ: ${a.p.label||''}`;
    case 'remed':return `ซ่อมจุดอ่อนก่อนสอบหน่วยที่ ${a.u} ใหม่`;
    case 'review':return 'ทบทวนสะสม 5 ข้อ จากแนวคิดที่ถึงรอบทบทวน';
    case 'step':return `หน่วยที่ ${a.u} · ${a.step.label}`;
    case 'finished':return 'ผ่านครบ 70 หน่วยแล้ว · ทบทวนจุดอ่อนต่อได้';
    case 'readonly':return 'เปิดแบบอ่านอย่างเดียว';
    default:return 'เริ่มเรียน';
  }
}
function runTitle(r){const lab={guided:'ฝึกพร้อมคำใบ้',assess:'แบบทดสอบท้ายหน่วย',remed:'ซ่อมจุดอ่อน',review:'ทบทวนสะสม',practice:'ฝึกด้วยตนเอง',extra:'ฝึกเพิ่ม'}[r.mode]||'';return (r.mode==='review'?'':'หน่วยที่ '+r.unit+' · ')+lab}
function cont(){
  const s=st();if(!idx()){toast('ยังโหลดหลักสูตรไม่สำเร็จ');return}
  const a=nextAction();
  switch(a.k){
    case 'resume':showRun();return;
    case 'external':relaunch();return;
    case 'remed':startRemed(a.u);return;
    case 'review':startReview();return;
    case 'step':return startStep(a.u,a.step.k);
    case 'complete-unit':completeUnit(a.u);renderHub();return;
    default:renderHub();
  }
}
function startStep(n,key){
  if(READONLY){toast(NOTICE);return}
  if(locked(n)){toast('ต้องผ่านหน่วยที่ '+st().unit+' ก่อน จึงจะเรียนหน่วยถัดไปได้');return}
  const u=unitDef(n),us=unitState(n);if(!u)return;
  if(st().active&&key!=='learn'){toast('มีแบบฝึกที่ค้างอยู่ ระบบพาไปทำต่อจากข้อเดิม');showRun();return}
  if(st().pending&&key!=='learn'&&!(st().pending.u===n&&st().pending.key===key)){toast('มีกิจกรรมจาก Learning Hub ที่ยังทำไม่จบ');renderHub();return}
  if(!us.started)us.started=now();
  const sp=steps(u),step=sp.find(x=>x.k===key);if(!step)return;
  // Sequential inside the current unit: earlier steps first (completed units can be revisited freely).
  if(us.st!=='done'){const firstOpen=sp.find(x=>!us.done[x.k]);if(firstOpen&&sp.indexOf(step)>sp.indexOf(firstOpen)){toast('ทำ “'+firstOpen.label+'” ก่อน');return}}
  if(us.remed&&us.remed.required&&key==='assess'){startRemed(n);return}
  if(key==='learn')return showLearn(n);
  if(key==='guided')return startGuided(n);
  if(key==='practice')return startPractice(n);
  if(key==='assess')return startAssess(n);
  if(step.act)return launchAct(n,key,step.act);
}

/* ------------------------------------------------------------------ runs (questions inside the hub) */
function needsBank(cs){return !Array.isArray(cs)||cs.some(c=>{const d=conceptDef(c);return Array.isArray(d.bank)&&d.bank.length>0})}
function withBank(fn,cs){if(bankReady()||(cs&&!needsBank(cs)))return fn();renderLoading('กำลังโหลดคลังข้อสอบ…');ensureBank().then(()=>{if(idx())idx().bankByC=null;fn()}).catch(e=>{toast(e&&e.message||'โหลดคลังข้อสอบไม่สำเร็จ');renderHub()})}
function makeRun(mode,n,refs,opt={}){
  const items=refs.map(r=>{const it=getItem(r);const len=it?it.opts.length:4;return {id:r.id,src:r.src,c:r.c||(it&&it.c)||'',o:shuffle([...Array(len).keys()]),rem:!!r.rem}});
  return {mode,unit:n,items,i:0,ans:[],phase:'q',conf:opt.conf||[],ins:0,lvl:opt.lvl||2,streak:0,started:now(),key:opt.key||mode};
}
function startRun(run){const s=st();s.active=run;const u=unitState(run.unit);if(run.mode!=='review'){u.used=(u.used||[]).concat(run.items.map(x=>x.id)).slice(-200)}save();showRun()}
function unitConcepts(u){return (u.concepts||[]).filter(Boolean)}
function startLevel(concepts){let best=0,n=0;concepts.forEach(c=>{const r=st().concepts[c];if(r&&r.a>=4){best+=r.k/r.a;n++}});const acc=n?best/n:0;return acc>=0.85?3:acc>=0.6?2:1}
function startGuided(n){const u=unitDef(n),g0=u.guided||{};withBank(()=>{
  const g=u.guided,ex=new Set();let refs=[];
  if(Array.isArray(g.ids))refs=g.ids.map(id=>{const it=idx().items.get(id);return it?{id,src:'hub',c:it.c}:null}).filter(Boolean);
  if(g.c){const cs=dyn(g.c,n),want=Math.max(0,(g.n||5)-refs.length);if(want){const per=Math.max(1,Math.ceil(want/cs.length)),lvl=startLevel(cs),extra=[];
    cs.forEach(c=>pick(c,per,{exclude:new Set([...ex,...refs.map(r=>r.id),...extra.map(r=>r.id)]),d:lvl}).forEach(r=>extra.push(r)));refs=refs.concat(extra.slice(0,want))}}
  if(!refs.length){toast('ยังไม่มีโจทย์สำหรับขั้นนี้');return}
  const conf=refs.length>=4?[1,3]:[0];
  startRun(makeRun('guided',n,refs,{conf,lvl:startLevel(unitConcepts(u)),key:'guided'}));
},g0.c?(Array.isArray(g0.c)?g0.c:null):unitConcepts(u))}
function startPractice(n){const u=unitDef(n);withBank(()=>{
  const p=u.practice,cs=dyn(p.c||unitConcepts(u),n),used=new Set(unitState(n).used||[]),refs=[];
  const per=Math.max(1,Math.ceil((p.n||8)/cs.length));cs.forEach(c=>pick(c,per,{exclude:new Set([...used,...refs.map(r=>r.id)]),src:p.src,d:2}).forEach(r=>refs.push(r)));
  if(!refs.length){toast('ยังไม่มีโจทย์สำหรับขั้นนี้');return}
  startRun(makeRun('practice',n,shuffle(refs).slice(0,p.n||8),{key:'practice'}));
})}
function dyn(spec,n){
  // dynamic concept lists for the strategy units
  if(spec==='errors'){const s=st();const byC={};Object.values(s.errors).forEach(e=>{if(e&&e.c&&e.wrong>0)byC[e.c]=(byC[e.c]||0)+e.wrong*(e.type==='misconception'?2:1)});
    let list=Object.entries(byC).sort((a,b)=>b[1]-a[1]).map(x=>x[0]).filter(c=>conceptPool(c).length>3).slice(0,4);
    if(list.length<2)list=list.concat(['tc.mixed','rc.mixed','conv.mixed'].filter(c=>!list.includes(c))).slice(0,4);return list}
  if(spec==='mock'){const p=st().units[n]&&st().units[n].mockWeak;const list=Array.isArray(p)&&p.length?p:['conv.mixed','tc.mixed','rc.mixed'];return list.slice(0,4)}
  return Array.isArray(spec)?spec:[spec];
}
function startAssess(n,retake){const u=unitDef(n);withBank(()=>{
  const us=unitState(n),a=u.assess||{},cs=dyn(a.c||unitConcepts(u),n),N=a.n||10;
  const prevIds=new Set((us.att||[]).flatMap(x=>x.ids||[]));const used=new Set(us.used||[]);
  const quota={};cs.forEach(c=>quota[c]=Math.max(2,Math.floor(N/cs.length)));
  let total=Object.values(quota).reduce((a,b)=>a+b,0),ci=0;while(total<N){quota[cs[ci%cs.length]]++;total++;ci++}
  const refs=[],chosen=new Set();const dCycle=[2,1,2,3,2,2,1,3];let dc=0;
  cs.forEach(c=>{let got=0;for(let k=0;k<quota[c]*3&&got<quota[c];k++){const ex=new Set([...chosen,...prevIds,...used]);let r=pick(c,1,{exclude:ex,d:dCycle[dc++%dCycle.length],src:a.src})[0];
    if(!r)r=pick(c,1,{exclude:new Set([...chosen,...prevIds]),src:a.src})[0];if(!r)r=pick(c,1,{exclude:chosen,src:a.src})[0];if(!r)break;chosen.add(r.id);refs.push(r);got++}});
  if(refs.length<Math.min(4,N)){toast('คลังโจทย์ของหน่วยนี้ยังไม่พอสำหรับแบบทดสอบ');return}
  const order=shuffle(refs);
  // Selective confidence: two "mastery check" items from different concepts.
  const conf=[];const seenC=new Set();order.forEach((r,i)=>{if(conf.length<2&&!seenC.has(r.c)){conf.push(i);seenC.add(r.c)}});
  if(conf.length<2&&order.length>2)conf.push(Math.floor(order.length/2));
  startRun(makeRun('assess',n,order,{conf,key:'assess'}));
},Array.isArray((u.assess||{}).c)?u.assess.c:((u.assess||{}).c?null:unitConcepts(u)))}
function startRemed(n){const u=unitDef(n);withBank(()=>{
  const us=unitState(n),cs=(us.remed&&us.remed.concepts&&us.remed.concepts.length?us.remed.concepts:unitConcepts(u)).slice(0,3);
  // new questions on the weak concepts; when a small pool runs out, reuse the least recently seen
  // items but never the questions of the assessment that was just failed
  const last=new Set(((us.att||[]).slice(-1)[0]||{}).ids||[]),used=new Set(us.used||[]),refs=[];const per=Math.max(2,Math.ceil(6/cs.length));
  cs.forEach(c=>{let got=pick(c,per,{exclude:new Set([...used,...last,...refs.map(r=>r.id)]),d:1});
    if(got.length<per)got=got.concat(pick(c,per-got.length,{exclude:new Set([...last,...refs.map(r=>r.id),...got.map(r=>r.id)]),d:1}));got.forEach(r=>refs.push(r))});
  if(!refs.length){us.remed.required=false;save();renderHub();return}
  startRun(makeRun('remed',n,refs.slice(0,6),{conf:[0,Math.min(refs.length,6)-1],lvl:1,key:'remed'}));
},(unitState(n).remed&&unitState(n).remed.concepts)||unitConcepts(u))}
function startReview(){withBank(()=>{
  const s=st(),cs=dueConcepts().slice(0,3);if(!cs.length){s.reviewDay=today();save();cont();return}
  const refs=[];let guard=0;while(refs.length<5&&guard<15){const c=cs[guard%cs.length];const r=pick(c,1,{exclude:new Set(refs.map(x=>x.id)),d:2})[0];if(r)refs.push(r);guard++}
  if(!refs.length){s.reviewDay=today();save();cont();return}
  startRun(makeRun('review',s.unit,refs,{conf:[0],key:'review'}));
})}
function startExtra(n){const u=unitDef(n);if(st().active){toast('มีแบบฝึกที่ค้างอยู่ ทำให้จบก่อน');return}withBank(()=>{
  const cs=unitConcepts(u),refs=[];cs.forEach(c=>pick(c,Math.ceil(6/cs.length),{exclude:new Set(refs.map(r=>r.id))}).forEach(r=>refs.push(r)));
  if(!refs.length){toast('ยังไม่มีโจทย์เพิ่มสำหรับหน่วยนี้');return}
  const s=st();s.active=makeRun('extra',n,shuffle(refs).slice(0,6),{key:'extra'});save();showRun();
})}
/* Full Coverage Practice: draw from ALL unseen bank items across every family, so
   completing the guided path + full-coverage sessions reaches all 1,200 questions. */
function startFullCoverage(){if(st().active){toast('มีแบบฝึกที่ค้างอยู่ ทำให้จบก่อน');return}withBank(()=>{
  const s=st(),used=new Set(),seenIds=new Set(Object.keys(s.seen));
  // collect all bank item ids across every concept family
  const allIds=[];const seenAll=new Set();
  Object.keys(idx().concepts).forEach(c=>{bankPool(c).forEach(id=>{if(!seenAll.has(id)){seenAll.add(id);allIds.push(id)}})});
  // filter: unseen first, then least recently seen
  const unseen=allIds.filter(id=>!seenIds.has(id));
  const recent=allIds.filter(id=>seenIds.has(id)).sort((a,b)=>{const sa=s.seen[a],sb=s.seen[b];return (sb.t-sa.t)});
  const refs=[];const pool=unseen.concat(recent).filter(id=>!used.has(id));
  // pick 10 items spread across families
  const byFam={};pool.forEach(id=>{const q=W.VLT_get(id);if(q){const f=family(q);(byFam[f]=byFam[f]||[]).push(id)}});
  const fams=Object.keys(byFam).sort((a,b)=>b.length-a.length);
  const per=Math.max(1,Math.floor(10/fams.length));let picked=0;
  fams.forEach(f=>{const take=Math.min(per,byFam[f].length,10-picked);shuffle(byFam[f]).slice(0,take).forEach(id=>{const q=W.VLT_get(id);if(q){refs.push({id,src:'bank',c:(idx().concepts[Object.keys(idx().concepts).find(c=>bankPool(c).includes(id))]||{}).t||'',o:shuffle([...Array(q.options.length).keys()])});picked++}})});
  if(refs.length<4){toast('ไม่มีโจทย์เพิ่มเติมให้ฝึกครบทุกข้อ');return}
  s.active=makeRun('extra',s.unit,shuffle(refs).slice(0,10),{key:'extra',label:'ฝึกครบทุกข้อ'});save();showRun();
})}
/* Count how many of the 1,200 bank items have been seen at least once. */
function coverageCount(){const s=st();const seen=new Set(Object.keys(s.seen));let total=0,seenCount=0;
  if(bankReady()){total=VLT_BANK.length;VLT_BANK.forEach(q=>{if(seen.has(q.id))seenCount++})}
  return {seen:seenCount,total:total,pct:total?Math.round(seenCount/total*100):0}}
const HINTS={guided:true,remed:true,review:true};
function current(){const r=st().active;if(!r)return null;const ref=r.items[r.i];return {r,ref,item:getItem(ref),a:r.ans[r.i]||(r.ans[r.i]={})}}
function needConf(r){return r.conf.includes(r.i)}
function pickOption(k){
  const cu=current();if(!cu||!cu.item)return;const {r,ref,item,a}=cu;const orig=r.items[r.i].o[k];
  if(r.mode==='assess'){a.s1=orig;save();renderRun();return}
  if(r.phase==='fb'||r.phase==='conf')return;
  if(r.phase==='hint'){if(orig===a.s1)return;a.s2=orig;a.ok2=orig===item.ans;evidence(ref.c||item.c,a.ok2,null,'hinted');r.phase='fb';save();renderRun(true);return}
  a.s1=orig;
  if(needConf(r)&&!a.cf){r.phase='conf';save();renderRun();return}
  judge();
}
function setConf(v){const cu=current();if(!cu)return;cu.a.cf=v;if(cu.r.mode==='assess'){save();renderRun();return}judge()}
function judge(){
  const {r,ref,item,a}=current();const c=ref.c||item.c;const ok=a.s1===item.ans;a.ok1=ok;a.t=now();
  evidence(c,ok,a.cf||null,'first');remember(ref,item,a.s1,ok,a.cf||null,r.mode);
  if(r.mode==='review')scheduleAfterReview(c,ok);
  if(ok){r.streak=(r.streak||0)+1;r.lvl=Math.min(3,r.streak>=2?r.lvl+1:r.lvl);r.phase='fb'}
  else{r.streak=0;r.lvl=Math.max(1,r.lvl-1);
    // adaptive remediation: one easier, unseen question on the same concept right after this one
    if(HINTS[r.mode]&&r.ins<2&&!ref.rem){const ex=new Set(r.items.map(x=>x.id));const nx=pick(c,1,{exclude:ex,d:Math.max(1,itemDifficulty(ref)-1)})[0];
      if(nx){const it=getItem(nx);r.items.splice(r.i+1,0,{id:nx.id,src:nx.src,c,o:shuffle([...Array(it?it.opts.length:4).keys()]),rem:true});r.ins++;
        if(r.mode!=='review'){const us=unitState(r.unit);us.used=(us.used||[]).concat(nx.id).slice(-200)}}}
    r.phase=HINTS[r.mode]&&Boolean(item.hint)?'hint':'fb'}
  save();renderRun(true);
}
function nextQ(){
  const r=st().active;if(!r)return;const a=r.ans[r.i]||{};
  if(r.mode==='assess'){if(!Number.isInteger(a.s1)){toast('เลือกคำตอบก่อน');return}if(needConf(r)&&!a.cf){toast('เลือกระดับความมั่นใจก่อน');return}}
  else if(r.phase!=='fb')return;
  // fast path inside guided practice for a strong learner: 3 first-try correct answers in a row
  if(r.mode==='guided'&&r.i>=2&&r.items.length-r.i>1){const last3=r.ans.slice(r.i-2,r.i+1);if(last3.length===3&&last3.every(x=>x&&x.ok1&&x.cf!=='not')&&!r.fastOffered){r.fastOffered=true;save();renderFast();return}}
  if(r.i<r.items.length-1){r.i++;r.phase='q';save();renderRun();scrollTop();return}
  finishRun();
}
function fastFinish(yes){const r=st().active;if(!r)return;if(yes){r.items=r.items.slice(0,r.i+1);finishRun();return}r.i++;r.phase='q';save();renderRun();scrollTop()}
function pauseRun(){save();renderHub()}
function finishRun(){
  const s=st(),r=s.active;if(!r)return;const n=r.unit,us=unitState(n);
  const res=r.items.map((ref,i)=>({ref,a:r.ans[i]||{}}));
  let score,total=res.length;
  if(r.mode==='assess'){
    res.forEach(({ref,a})=>{const it=getItem(ref);if(!it)return;const ok=a.s1===it.ans;a.ok1=ok;evidence(ref.c||it.c,ok,a.cf||null,'first');remember(ref,it,a.s1,ok,a.cf||null,'assess')});
    score=res.filter(x=>x.a.ok1).length;
    const byC={};res.forEach(({ref,a})=>{const c=ref.c;byC[c]=byC[c]||{k:0,t:0,low:0};byC[c].t++;if(a.ok1)byC[c].k++;if(a.ok1&&a.cf==='not')byC[c].low++});
    const pct=Math.round(score/total*100);
    const weak=Object.entries(byC).filter(([c,v])=>v.t>=2?v.k/v.t<0.5:v.k===0).map(([c])=>c);
    const pass=pct>=PASS_PCT&&!weak.length;
    const low=Object.entries(byC).filter(([c,v])=>v.low>0).map(([c])=>c);
    const wrong=res.filter(x=>!x.a.ok1).map(({ref,a})=>{const it=getItem(ref);return it?{id:ref.id,stem:String(it.stem).slice(0,200),sel:Number.isInteger(a.s1)?String(it.opts[a.s1]):'',ans:String(it.opts[it.ans]),why:String(it.why||'').slice(0,400)}:null}).filter(Boolean);
    const rec={t:now(),u:n,k:score,n:total,pct,pass,c:byC,low,ids:res.map(x=>x.ref.id),weak,wrong};
    us.att.push(rec);s.assessments.push({t:rec.t,u:n,k:score,n:total,pct,pass});
    if(pass){us.done.assess=true;us.res.assess={score,total,pct,at:now()};us.remed=null;
      low.forEach(c=>{const cr=cRec(c);cr.p=clamp(cr.p+2,0,20);cr.due=now()+DAY;cr.du=n+1});
      Object.keys(byC).forEach(c=>{const cr=cRec(c);if(cr.st==='learning'||cr.st==='new'){cr.st='review';cr.iv=cr.iv||1;cr.due=cr.due||now()+DAY;cr.du=cr.du||n+2}});
      log({k:'assess',u:n,pct,pass:true});
      const sp=steps(unitDef(n));if(sp.every(x=>us.done[x.k]))completeUnit(n);
    }else{us.remed={required:true,concepts:weak.length?weak:Object.keys(byC),at:now()};log({k:'assess',u:n,pct,pass:false})}
    s.active=null;s.lastResult={mode:'assess',u:n,rec};save();renderAssessResult(rec);return;
  }
  score=res.filter(x=>x.a.ok1).length;
  if(r.mode==='guided'||r.mode==='practice'){us.done[r.key]=true;us.res[r.key]={score,total,pct:Math.round(score/total*100),at:now()};log({k:r.key,u:n,score,total})}
  if(r.mode==='remed'&&us.remed){us.remed.required=false;us.remed.doneAt=now();log({k:'remed',u:n,score,total})}
  if(r.mode==='review'){s.reviewDay=today();log({k:'review',u:s.unit,score,total})}
  if(r.mode==='extra')log({k:'extra',u:n,score,total});
  s.active=null;s.lastResult={mode:r.mode,u:n,score,total};save();renderRunDone(r.mode,n,score,total);
}
function completeUnit(n){
  const s=st(),us=unitState(n);if(us.st==='done')return;
  us.st='done';us.completed=now();log({k:'unit',u:n});
  if(n<UNITS){s.unit=n+1;unitState(n+1).started=0}
  try{if(typeof VLT_STATE!=='undefined'&&VLT_STATE){VLT_STATE.xp=(Number(VLT_STATE.xp)||0)+30;if(typeof W.VLT_save==='function')W.VLT_save()}}catch(_){}
  save();
}

/* ------------------------------------------------------------------ external activities (existing systems) */
function readJSON(k,f){try{const v=JSON.parse(localStorage.getItem(k)||'null');return v==null?f:v}catch(_){return f}}
function snapshot(a){if(a.type==='phrase')return readJSON('tgat1_studio_everyday_phrase_v382',{attempts:0,correct:0});return null}
function launchAct(n,key,a){
  const s=st();if(s.active){toast('มีแบบฝึกใน Learning Hub ค้างอยู่ ทำให้จบก่อน');return}
  s.pending={u:n,key,type:a.type,ref:a.ref??null,label:a.label||ACT_LABEL[a.type]||'',at:now(),snap:snapshot(a),cmap:null,result:null};s.returnTo=true;
  const begin=()=>{
    switch(a.type){
      case 'vlt':{const cs=dyn(a.c,n),refs=[],used=new Set(unitState(n).used||[]);const per=Math.ceil((a.n||10)/cs.length);
        cs.forEach(c=>pick(c,per,{exclude:new Set([...used,...refs.map(r=>r.id)]),src:'bank'}).forEach(r=>refs.push(r)));
        const qs=shuffle(refs).slice(0,a.n||10).map(r=>W.VLT_get(r.id)).filter(Boolean).map(q=>{const opts=shuffle(q.options.map((text,i)=>({text,correct:i===q.answer})));return {...q,options:opts.map(x=>x.text),answer:opts.findIndex(x=>x.correct)}});
        if(!qs.length){s.pending=null;save();toast('ไม่พบโจทย์สำหรับกิจกรรมนี้');return}
        s.pending.cmap=Object.fromEntries(refs.map(r=>[r.id,r.c]));unitState(n).used=(unitState(n).used||[]).concat(qs.map(q=>q.id)).slice(-200);save();
        try{STUDIO_PAGE='exam';W.studioUpdateChrome('exam')}catch(_){}
        W.VLT_begin({mode:'practice',label:'Learning Hub · หน่วยที่ '+n+' · '+(a.label||''),qs:qs.map(q=>({...q,userAnswer:null})),index:0,answers:{},score:0,combo:0,reviewOn:false,hub:{u:n,key}});return}
      case 'mock':{const sets=(typeof VLT_STATE!=='undefined'&&VLT_STATE.completedSets)||{};let best=a.ref||1,att=1e9;
        for(let i=1;i<=20;i++){const x=sets[i];const k=x?x.attempts||1:0;if(k<att){att=k;best=i}}
        s.pending.ref=best;save();W.VLT_startMock(best);return}
      case 'grammar':save();try{STUDIO_PAGE='grammar';W.studioUpdateChrome('grammar')}catch(_){}W.STG_start(Number(a.ref)||0);return;
      case 'readingPlus':save();W.TGAT1ReadingPlus.start(String(a.ref));return;
      case 'vocab':save();try{STUDIO_PAGE='game';W.studioUpdateChrome('game')}catch(_){}try{const old=S.cur;S.cur='B';W.studioRunVocabGame(String(a.ref||'match'));S.cur=old||'A'}catch(e){W.studioRunVocabGame(String(a.ref||'match'))}return;
      case 'phrase':save();try{STUDIO_PAGE='vocab';W.studioUpdateChrome('vocab')}catch(_){}W.TGAT1PhrasePlus.start(a.ref||'All');return;
    }
    s.pending=null;save();toast('ไม่รู้จักกิจกรรมนี้');
  };
  if(a.type==='vlt'||a.type==='mock')withBank(begin);else begin();
  updateBanner();
}
function relaunch(){const p=st().pending;if(!p)return renderHub();const u=unitDef(p.u);const step=u&&steps(u).find(x=>x.k===p.key);if(!step){st().pending=null;save();return renderHub()}st().pending=null;launchAct(p.u,p.key,step.act)}
function cancelPending(){const s=st();s.pending=null;save();renderHub()}
// Completion is read from each system's own saved progress, so a step is never marked done unless the activity really finished.
function verifyPending(){
  const s=st(),p=s.pending;if(!p)return null;
  let res=p.result||null;
  if(!res&&p.type==='grammar'){const g=readJSON('tgat1_studio_grammar_clinic_v1',{});const rows=(g.history||[]).filter(h=>Number(h.topic)===Number(p.ref)&&Number(h.at)>=p.at);
    const qset=new Set(rows.map(h=>h.question));if(qset.size>=5){const latest={};rows.forEach(h=>latest[h.question]=h);const vals=Object.values(latest);res={score:vals.filter(h=>h.correct).length,total:vals.length}}}
  if(!res&&p.type==='readingPlus'){const rs=readJSON('tgat1_studio_reading_plus_v382',{});const x=rs[p.ref];if(x&&Number(x.lastAt)>=p.at)res={score:Math.round((Number(x.lastPercent)||0)/100*(Number(x.total)||5)),total:Number(x.total)||5,pct:Number(x.lastPercent)||0}}
  if(!res&&p.type==='phrase'){const now2=readJSON('tgat1_studio_everyday_phrase_v382',{attempts:0,correct:0}),was=p.snap||{attempts:0,correct:0};
    const dn=(Number(now2.attempts)||0)-(Number(was.attempts)||0);if(dn>=5){const k=(Number(now2.correct)||0)-(Number(was.correct)||0);res={score:clamp(k,0,dn),total:dn}}}
  if(!res)return null;
  const us=unitState(p.u);const total=Math.max(1,res.total||1),pct=res.pct!=null?Math.round(res.pct):Math.round((res.score||0)/total*100);
  us.done[p.key]=true;us.res[p.key]={score:res.score,total,pct,at:now(),type:p.type};
  const u=unitDef(p.u);if(pct<60&&u)unitConcepts(u).forEach(c=>{const r=cRec(c);r.p=clamp(r.p+1,0,20)});
  log({k:'act',u:p.u,type:p.type,pct});try{const vs=W.VLT_STATE;if(vs){vs.xp=(Number(vs.xp)||0)+5;const d=today(),y=new Date(Date.now()-DAY),yd=y.getFullYear()+'-'+String(y.getMonth()+1).padStart(2,'0')+'-'+String(y.getDate()).padStart(2,'0');if(vs.lastDay!==d){vs.streak=vs.lastDay===yd?(Number(vs.streak)||0)+1:1;vs.lastDay=d}if(typeof W.VLT_updateBadges==='function')W.VLT_updateBadges();if(typeof W.VLT_save==='function')W.VLT_save()}}catch(e){console.warn('Hub XP/streak update skipped',e)}s.pending=null;s.returnTo=true;save();return res;
}
function onVltFinished(r){
  const s=st(),p=s.pending;if(!r||!p)return;
  if(p.type==='vlt'&&r.hub&&r.hub.u===p.u&&r.hub.key===p.key){
    let k=0,t=0;(r.qs||[]).forEach(q=>{const a=r.answers&&r.answers[q.id];if(!Number.isInteger(a))return;t++;const ok=a===q.answer;if(ok)k++;
      const c=(p.cmap&&p.cmap[q.id])||'';if(c){evidence(c,ok,null,'first');const it=bankItem(q.id);if(it){s.seen[q.id]={n:((s.seen[q.id]||{}).n||0)+1,t:now()};if(!ok){const row=s.errors[q.id]||{qid:q.id,src:'bank',c,skill:conceptDef(c).skill||'',att:0,wrong:0,recent:[],first:now()};row.att++;row.wrong++;row.recent=(row.recent||[]).concat(0).slice(-6);row.type='error';row.sel=Array.isArray(q.options)?q.options[a]:it.opts[a];row.ans=Array.isArray(q.options)?q.options[q.answer]:it.opts[it.ans];row.why=String(it.why||'').slice(0,600);row.last=now();row.mode='vlt';row.unit=p.u;s.errors[q.id]=row}}}});
    p.result={score:k,total:Math.max(1,t)};save();verifyPending();updateBanner();return;
  }
  if(p.type==='mock'&&r.mode==='mock'&&Number(r.setNo)===Number(p.ref)){
    const fam={};(r.qs||[]).forEach(q=>{const f=family(q);fam[f]=fam[f]||{k:0,t:0};fam[f].t++;if(r.answers&&r.answers[q.id]===q.answer)fam[f].k++});
    const toConcept=f=>f.startsWith('tc.')?'tc.mixed':f.startsWith('rc.')?'rc.mixed':'conv.mixed';
    const agg={};Object.entries(fam).forEach(([f,v])=>{const c=toConcept(f);agg[c]=agg[c]||{k:0,t:0};agg[c].k+=v.k;agg[c].t+=v.t});
    unitState(p.u).mockWeak=Object.entries(agg).sort((a,b)=>a[1].k/a[1].t-b[1].k/b[1].t).map(x=>x[0]);
    const k=(r.qs||[]).filter(q=>r.answers&&r.answers[q.id]===q.answer).length;
    p.result={score:k,total:(r.qs||[]).length||60};save();verifyPending();updateBanner();
  }
}
function onGameFinished(q){const p=st().pending;if(!q||!p||p.type!=='vocab'||!['game','free'].includes(q.mode))return;const match=String(q.again||'').match(/play\(['\"]([^'\"]+)['\"]\)/);if(p.ref&&match&&String(p.ref)!==match[1])return;const total=Array.isArray(q.qs)?q.qs.length:0;if(total<4)return;p.result={score:Number(q.ok)||0,total};save();verifyPending();updateBanner()}

/* ------------------------------------------------------------------ rendering */
function app(){return D.getElementById('app')}
function scrollTop(){try{W.scrollTo({top:0,behavior:'auto'})}catch(_){}}
function chrome(sub){try{if(page()!=='hub'){STUDIO_PAGE='hub'}W.studioUpdateChrome('hub');const t=D.getElementById('studioTitle');if(t&&sub)t.textContent=sub}catch(_){}}
function renderLoading(msg){const el=app();if(!el)return;chrome();el.innerHTML=`<div class="st-card lh-card" role="status">${esc(msg)}</div>`}
function bar(p,label){return `<div class="lh-bar" role="progressbar" aria-label="${esc(label||'ความคืบหน้า')}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${Math.round(p)}"><i style="width:${clamp(p,0,100)}%"></i></div>`}
function phaseOf(n){const c=cur();return c?(c.phases||[]).find(p=>n>=p.from&&n<=p.to):null}
function skillSummary(){
  const s=st(),by={};Object.entries(s.concepts).forEach(([c,r])=>{if(!isObj(r)||!r.a)return;const sk=conceptDef(c).skill||'mixed';by[sk]=by[sk]||{a:0,k:0};by[sk].a+=r.a;by[sk].k+=r.k});
  return by;
}
const SKILL_TH={structure:'โครงสร้างประโยค',grammar:'ไวยากรณ์',vocab:'คำศัพท์',logic:'ตรรกะประโยค/คำเชื่อม',conversation:'บทสนทนา',cloze:'เติมคำในบทความ',reading:'การอ่าน',strategy:'กลยุทธ์ข้อสอบ',mixed:'ผสม'};
const ST_TH={new:'ยังไม่เริ่ม',learning:'กำลังเรียน',review:'รอทบทวน',mastered:'เชี่ยวชาญแล้ว'};
const TYPE_TH={misconception:'เข้าใจผิด (ตอบผิดแต่มั่นใจ)','knowledge-gap':'ยังไม่รู้ (ผิดและไม่มั่นใจ)',guess:'ถูกแต่ไม่มั่นใจ',slip:'พลาดในเรื่องที่เคยทำได้',error:'ตอบผิด'};
function fmtDate(t){if(!t)return'-';const d=new Date(t);return d.getDate()+'/'+(d.getMonth()+1)+' '+String(d.getHours()).padStart(2,'0')+':'+String(d.getMinutes()).padStart(2,'0')}
function renderHub(){
  const el=app();if(!el)return;chrome('Learning Hub · เส้นทาง 70 หน่วย');
  if(!cur()){el.innerHTML=`<div class="st-card lh-card" role="alert">โหลดหลักสูตร Learning Hub ไม่สำเร็จ ลองรีเฟรชหน้า</div>`;return}
  const s=st();if(s.pending)verifyPending();s.returnTo=false;save();updateBanner();
  const a=nextAction(),n=s.unit,u=unitDef(n),us=unitState(n),doneUnits=Object.values(s.units).filter(x=>x.st==='done').length;
  const ph=phaseOf(n),sp=steps(u),con=Object.entries(s.concepts).filter(([c,r])=>isObj(r)&&r.a>0);
  const mastered=con.filter(([c,r])=>r.st==='mastered'),due=dueConcepts();
  const errs=Object.values(s.errors).filter(e=>e&&e.wrong>0);
  const errByC={};errs.forEach(e=>{errByC[e.c]=(errByC[e.c]||0)+e.wrong});
  const topErr=Object.entries(errByC).sort((a,b)=>b[1]-a[1]).slice(0,5);
  const sk=skillSummary();
  const cov=coverageCount();
  const actBtn=a.k==='finished'?`<button type="button" class="st-btn lh-cta" data-action="TGAT1Hub.review">ทบทวนจุดอ่อน</button>`:`<button type="button" class="st-btn lh-cta" data-action="TGAT1Hub.continue" ${READONLY?'disabled':''}><span>เรียนต่อ</span><small>Continue Learning</small></button>`;
  el.innerHTML=`
  ${NOTICE?`<div class="st-card lh-notice" role="status">${esc(NOTICE)}</div>`:''}
  <section class="st-card lh-main" aria-labelledby="lhHeroTitle">
    <div class="st-eyebrow">PERSONALIZED 70-UNIT PATH</div>
    <h1 class="st-title" id="lhHeroTitle">หน่วยที่ ${n} · ${esc(u?u.title:'')}</h1>
    <p class="st-subtitle">${esc(ph?('ช่วงที่ '+ph.id+' · '+ph.title):'')}${u&&u.en?' · '+esc(u.en):''}</p>
    <div class="lh-progress-row"><span>ผ่านแล้ว <b>${doneUnits}</b> / ${UNITS} หน่วย</span>${bar(doneUnits/UNITS*100)}</div>
    ${cov.total?`<div class="lh-progress-row"><span>ข้อสอบที่เคยทำ <b>${cov.seen}</b> / ${cov.total} ข้อ · ${cov.pct}%</span>${bar(cov.pct)}</div>`:''}
    <section class="lh-vocab-shortcut"><div><div class="st-eyebrow">TGAT1 EXAM VOCABULARY</div><b>ศัพท์จากบริบทข้อสอบ + ระบบทบทวนแบบเว้นระยะ</b><p class="lh-mini">ฝึกคำที่พบในโจทย์ฝึกและวลีเป้าหมาย · ไม่เปลี่ยนคะแนนหรือเงื่อนไขผ่านหน่วย</p></div><button type="button" class="st-btn small" data-action="TGAT1VocabularyLab.start" data-arg="hub">ฝึกศัพท์ 10 ข้อ →</button></section>
    ${cov.total&&cov.pct<100?`<section class="lh-vocab-shortcut"><div><div class="st-eyebrow">FULL BANK COVERAGE</div><b>ฝึกครบทุก ${cov.total} ข้อสอบในคลัง</b><p class="lh-mini">ดึงข้อสอบที่ยังไม่เคยทำจากทุกหมวดหมู่ · ครบ 1,200 ข้อเมื่อเรียน hub + ฝึกครบทุกข้อ</p></div><button type="button" class="st-btn small" data-action="TGAT1Hub.fullCoverage">ฝึกครบทุกข้อ 10 ข้อ →</button></section>`:''}
    <ol class="lh-steps" aria-label="ขั้นตอนของหน่วยที่ ${n}">${sp.map(x=>`<li class="${us.done[x.k]?'done':''}${a.k==='step'&&a.step.k===x.k?' now':''}"><span aria-hidden="true">${us.done[x.k]?'✓':'•'}</span>${esc(x.label)}</li>`).join('')}</ol>
    <div class="lh-next"><div><small>ขั้นต่อไป</small><b>${esc(describe(a))}</b></div>${actBtn}</div>
    ${a.k==='external'?`<p class="lh-mini">กิจกรรมนี้อยู่ในระบบเดิมของแอป ระบบจะนับว่าเสร็จเมื่อทำครบในระบบนั้น · <button type="button" class="lh-link" data-action="TGAT1Hub.cancelPending">ยกเลิกกิจกรรมนี้ไว้ก่อน</button></p>`:''}
    <p class="lh-mini">Learning Hub เป็นเส้นทางแนะนำ ทุกหน้าอื่นในแอปยังเปิดใช้ได้ตามปกติ</p>
  </section>
  <div class="lh-grid">
    <section class="st-card lh-card" aria-labelledby="lhM"><h2 id="lhM">แนวคิด</h2>
      <div class="lh-kpis"><div><b>${mastered.length}</b><small>เชี่ยวชาญแล้ว</small></div><div><b>${con.length-mastered.length}</b><small>กำลังเรียน/รอทบทวน</small></div><div><b>${due.length}</b><small>ถึงรอบทบทวน</small></div></div>
      ${due.length?`<p class="lh-mini">ถึงรอบทบทวน: ${due.slice(0,4).map(c=>esc(conceptDef(c).t)).join(' · ')}</p><button type="button" class="st-btn ghost small" data-action="TGAT1Hub.review">ทบทวนตอนนี้</button>`:'<p class="lh-mini">ยังไม่มีแนวคิดที่ถึงรอบทบทวน</p>'}
    </section>
    <section class="st-card lh-card" aria-labelledby="lhE"><h2 id="lhE">ความจำข้อผิดพลาด</h2>
      <p class="lh-mini">${errs.length} ข้อที่เคยผิด จาก ${new Set(errs.map(e=>e.c)).size} แนวคิด</p>
      ${topErr.length?`<ul class="lh-list">${topErr.map(([c,k])=>{const r=s.concepts[c]||{};return `<li><span>${esc(conceptDef(c).t)}</span><small>ผิด ${k} ครั้ง · ${esc(ST_TH[r.st]||'')}</small></li>`}).join('')}</ul><button type="button" class="st-btn ghost small" data-action="TGAT1Hub.showErrors">ดูทั้งหมด</button>`:'<p class="lh-mini">ยังไม่มีข้อผิดที่บันทึกไว้</p>'}
    </section>
    <section class="st-card lh-card" aria-labelledby="lhS"><h2 id="lhS">ผลรายทักษะ</h2>
      ${Object.keys(sk).length?`<ul class="lh-list">${Object.entries(sk).map(([k,v])=>`<li><span>${esc(SKILL_TH[k]||k)}</span><small>${Math.round(v.k/v.a*100)}% · ${v.a} ข้อ</small></li>`).join('')}</ul>`:'<p class="lh-mini">จะแสดงหลังเริ่มทำโจทย์</p>'}
    </section>
    <section class="st-card lh-card" aria-labelledby="lhA"><h2 id="lhA">แบบทดสอบท้ายหน่วยล่าสุด</h2>
      ${s.assessments.length?`<ul class="lh-list">${s.assessments.slice(-5).reverse().map(x=>`<li><span>หน่วยที่ ${x.u}</span><small>${x.k}/${x.n} · ${x.pct}% · ${x.pass?'ผ่าน':'ยังไม่ผ่าน'}</small></li>`).join('')}</ul>`:'<p class="lh-mini">ยังไม่มี</p>'}
    </section>
    <section class="st-card lh-card" aria-labelledby="lhR"><h2 id="lhR">กิจกรรมล่าสุด</h2>
      ${s.history.length?`<ul class="lh-list">${s.history.slice(-6).reverse().map(h=>`<li><span>${esc(histText(h))}</span><small>${fmtDate(h.t)}</small></li>`).join('')}</ul>`:'<p class="lh-mini">ยังไม่มี</p>'}
    </section>
  </div>
  <section class="st-card lh-card" aria-labelledby="lhMap"><h2 id="lhMap">แผนที่ 70 หน่วย</h2>
    <p class="lh-mini">เรียนตามลำดับ หน่วยถัดไปจะเปิดเมื่อผ่านแบบทดสอบท้ายหน่วยก่อนหน้า หน่วยที่ผ่านแล้วเปิดทบทวนได้เสมอ</p>
    ${(cur().phases||[]).map(p=>`<details class="lh-phase" ${n>=p.from&&n<=p.to?'open':''}><summary>ช่วงที่ ${p.id} · ${esc(p.title)} <small>หน่วย ${p.from}–${p.to}</small></summary><div class="lh-units">${
      Array.from({length:p.to-p.from+1},(_,i)=>p.from+i).map(k=>{const uu=unitDef(k),ust=s.units[k],dn=ust&&ust.st==='done',lk=locked(k);
        return `<button type="button" class="lh-unit ${dn?'done':lk?'locked':'current'}" data-action="TGAT1Hub.openUnit" data-arg="${k}" ${lk?'aria-disabled="true"':''} ><span class="lh-unit-n" aria-hidden="true">${dn?'✓':lk?'🔒':k}</span><span class="lh-unit-t">${k}. ${esc(uu?uu.title:'')}</span><span class="lh-sr"> · ${dn?'ผ่านแล้ว':lk?'ยังล็อก':'กำลังเรียน'}</span></button>`}).join('')}</div></details>`).join('')}
  </section>`;
}
function histText(h){switch(h.k){case'unit':return 'ผ่านหน่วยที่ '+h.u;case'assess':return 'แบบทดสอบหน่วยที่ '+h.u+' · '+h.pct+'% '+(h.pass?'ผ่าน':'ยังไม่ผ่าน');case'guided':return 'ฝึกพร้อมคำใบ้ หน่วยที่ '+h.u+' · '+h.score+'/'+h.total;
  case'practice':return 'ฝึกด้วยตนเอง หน่วยที่ '+h.u+' · '+h.score+'/'+h.total;case'remed':return 'ซ่อมจุดอ่อน หน่วยที่ '+h.u;case'review':return 'ทบทวนสะสม '+h.score+'/'+h.total;case'act':return 'กิจกรรม '+(ACT_LABEL[h.type]||'')+' หน่วยที่ '+h.u+' · '+h.pct+'%';case'learn':return 'เรียนแนวคิด หน่วยที่ '+h.u;case'vocab':return 'ฝึกศัพท์หน่วยที่ '+h.u+' · '+h.score+'/'+h.total;case'extra':return 'ฝึกเพิ่ม หน่วยที่ '+h.u;default:return h.k}}
function vocabBlock(n){
  const rows=window.TGAT1VocabularyLab&&typeof window.TGAT1VocabularyLab.unitWords==='function'?window.TGAT1VocabularyLab.unitWords(n):[];
  if(!rows||!rows.length)return '';
  return `<section class="lh-vocab-block"><div><div class="st-eyebrow">OPTIONAL · TGAT1 VOCABULARY</div><h2 class="lh-h">ศัพท์เป้าหมายของหน่วยนี้</h2><p class="lh-mini">ฝึกจากบริบทและบันทึกลงคลังทบทวนศัพท์แยกจากคะแนนข้อสอบ</p></div><div class="lh-vocab-words">${rows.map(x=>`<button type="button" class="lh-vocab-word" data-action="TGAT1VocabularyLab.openTerm" data-arg="${esc(JSON.stringify(x.w))}"><b>${esc(x.w)}</b><small>${esc(x.th)}</small></button>`).join('')}</div><button type="button" class="st-btn secondary small" data-action="TGAT1VocabularyLab.start" data-arg="unit" data-arg="${n}">ฝึกศัพท์หน่วยที่ ${n} →</button></section>`;
}
function openUnit(n){
  if(locked(n)){toast('หน่วยที่ '+n+' ยังล็อกอยู่ · ต้องผ่านหน่วยที่ '+st().unit+' ก่อน');return}
  const el=app(),u=unitDef(n),us=unitState(n);if(!el||!u)return;chrome('หน่วยที่ '+n);
  const sp=steps(u),firstOpen=us.st==='done'?null:sp.find(x=>!us.done[x.k]);
  el.innerHTML=`<div class="lh-top"><button type="button" class="st-btn ghost small" data-action="TGAT1Hub.open">← Learning Hub</button></div>
  <section class="st-card lh-card"><div class="st-eyebrow">หน่วยที่ ${n} · ${esc((phaseOf(n)||{}).title||'')}</div><h1 class="st-title">${esc(u.title)}</h1><p class="st-subtitle">${esc(u.en||'')}</p>
   <h2 class="lh-h">เป้าหมายของหน่วย</h2><ul class="lh-obj">${(u.obj||[]).map(o=>`<li>${esc(o)}</li>`).join('')}</ul>
   ${vocabBlock(n)}
   <h2 class="lh-h">ขั้นตอน</h2><ol class="lh-steplist">${sp.map(x=>{const r=us.res[x.k];const can=us.st==='done'||x===firstOpen||us.done[x.k];
     return `<li class="${us.done[x.k]?'done':''}"><div><b>${esc(x.label)}</b>${x.act&&x.act.note?`<small>${esc(x.act.note)}</small>`:''}${r?`<small>ผล: ${r.score}/${r.total} (${r.pct}%)</small>`:''}</div>${can?`<button type="button" class="st-btn small ${us.done[x.k]?'ghost':''}" data-action="TGAT1Hub.step" data-arg="${n}" data-arg="${x.k}">${us.done[x.k]?(x.k==='learn'?'อ่านอีกครั้ง':x.k==='assess'?'ดูผล':'ทำซ้ำ'):'เริ่ม'}</button>`:'<small>ทำขั้นก่อนหน้าก่อน</small>'}</li>`}).join('')}</ol>
   ${us.st==='done'?`<button type="button" class="st-btn ghost" data-action="TGAT1Hub.extra" data-arg="${n}">ฝึกเพิ่ม 6 ข้อ (ไม่กระทบความคืบหน้า)</button>`:''}
   ${us.att&&us.att.length?`<h2 class="lh-h">ประวัติแบบทดสอบ</h2><ul class="lh-list">${us.att.slice(-5).reverse().map(x=>`<li><span>${fmtDate(x.t)}</span><small>${x.k}/${x.n} · ${x.pct}% · ${x.pass?'ผ่าน':'ยังไม่ผ่าน'}</small></li>`).join('')}</ul>`:''}
  </section>`;scrollTop();
}
function stepEntry(n,key){
  const us=unitState(n);
  if(us.done[key]&&key==='assess'){const last=(us.att||[]).filter(x=>x.pass).slice(-1)[0];if(last)return renderAssessResult(last,true)}
  if(us.done[key]&&key!=='learn'&&us.st!=='done'&&key!=='assess'){/* redoing a finished step of the current unit is allowed as extra practice */}
  return startStep(n,key);
}
function showLearn(n){
  const el=app(),u=unitDef(n),L=u.learn||{};chrome('หน่วยที่ '+n+' · เรียนแนวคิด');
  el.innerHTML=`<div class="lh-top"><button type="button" class="st-btn ghost small" data-action="TGAT1Hub.openUnit" data-arg="${n}">← หน่วยที่ ${n}</button></div>
  <article class="st-card lh-card lh-learn"><div class="st-eyebrow">หน่วยที่ ${n} · เรียนแนวคิด</div><h1 class="st-title">${esc(u.title)}</h1>
   <h2 class="lh-h">เป้าหมาย</h2><ul class="lh-obj">${(u.obj||[]).map(o=>`<li>${esc(o)}</li>`).join('')}</ul>
   ${vocabBlock(n)}
   ${L.intro?`<p class="lh-p">${esc(L.intro)}</p>`:''}
   ${L.steps&&L.steps.length?`<h2 class="lh-h">ขั้นตอนคิด</h2><ol class="lh-reason">${L.steps.map(x=>`<li>${esc(x)}</li>`).join('')}</ol>`:''}
   ${L.rules&&L.rules.length?`<h2 class="lh-h">หลักที่ต้องจำให้แม่น</h2><ul class="lh-rules">${L.rules.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`:''}
   ${L.ex&&L.ex.length?`<h2 class="lh-h">ตัวอย่างวิเคราะห์ทีละขั้น</h2>${L.ex.map((x,i)=>`<div class="lh-example"><p class="lh-en" lang="en">${esc(x.en)}</p>${x.th?`<p class="lh-th">${esc(x.th)}</p>`:''}<ol>${(x.a||[]).map(s=>`<li>${esc(s)}</li>`).join('')}</ol></div>`).join('')}`:''}
   ${L.traps&&L.traps.length?`<h2 class="lh-h">กับดักที่พบบ่อย</h2><ul class="lh-traps">${L.traps.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`:''}
   <div class="lh-actions"><button type="button" class="st-btn" data-action="TGAT1Hub.learnDone" data-arg="${n}">เข้าใจแล้ว ไปขั้นถัดไป →</button></div>
  </article>`;scrollTop();
}
function learnDone(n){const us=unitState(n);if(!us.done.learn){us.done.learn=true;log({k:'learn',u:n});save()}if(us.st==='done')return openUnit(n);cont()}
function optionLabel(item,origIdx){
  // structural label for bank items so the learner can eliminate by form
  const t=String(item.opts[origIdx]||'').trim();if(item.src!=='bank')return'';
  const posLookup={during:'บุพบท (ระหว่างช่วงเวลา)',lonely:'คำคุณศัพท์ (โดดเดี่ยว)',only:'คำขยาย/คำจำกัดความ (เท่านั้น)',offer:'คำนามหรือกริยา (ข้อเสนอ/เสนอ)',differ:'กริยา (แตกต่าง)',volunteer:'คำนามหรือกริยา (อาสาสมัคร/อาสา)',after:'บุพบท/คำเชื่อม/คำวิเศษณ์ (หลังจาก)',another:'คำกำหนดนาม (อีกหนึ่ง/อีกคน)',otherwise:'คำวิเศษณ์/คำเชื่อม (มิฉะนั้น)',besides:'คำวิเศษณ์/บุพบท (นอกจากนี้/นอกจาก)'};if(posLookup[t.toLowerCase()])return posLookup[t.toLowerCase()];
  if(item.fam&&item.fam.startsWith('qr.')){if(/\d{1,2}:\d{2}|a\.m\.|p\.m\.|o.clock/i.test(t))return'บอกเวลา (What time)';if(/\b(once|twice|times a|every|always|usually|daily|weekly)\b/i.test(t))return'บอกความถี่ (How often)';if(/^for\b|\bhours?\b|\bminutes?\b|\bdays\b|takes/i.test(t))return'บอกระยะเวลา (How long)';if(/^(in|at|on|near|by)\s/i.test(t))return'บอกสถานที่ (Where)';if(/^since\b/i.test(t))return'บอกจุดเริ่มต้น (Since when)';return''}
  if(item.fam&&item.fam.startsWith('tc.')&&!/\s/.test(t)){if(/ing$/i.test(t))return'V-ing';if(/ly$/i.test(t))return'adverb (-ly)';if(/(tion|ment|ness|ity|ance|ence)$/i.test(t))return'noun';if(/ed$/i.test(t))return'V2/V3 (-ed)';if(/(er|est)$/i.test(t))return'เปรียบเทียบ?';}
  return'';
}
function renderFast(){
  const el=app();el.innerHTML=`<section class="st-card lh-card" role="status"><div class="st-eyebrow">ทำได้ดีมาก</div><h1 class="st-title">ตอบถูกตั้งแต่ครั้งแรก 3 ข้อติด</h1><p class="lh-p">ถ้ามั่นใจแล้ว ข้ามข้อที่เหลือของขั้นนี้ไปขั้นถัดไปได้ (ยังต้องทำแบบทดสอบท้ายหน่วยตามปกติ ไม่ข้ามหน่วย)</p>
  <div class="lh-actions"><button type="button" class="st-btn" data-action="TGAT1Hub.fast" data-arg="true">ไปขั้นถัดไป</button><button type="button" class="st-btn ghost" data-action="TGAT1Hub.fast" data-arg="false">ฝึกต่อให้ครบ</button></div></section>`;
}
function showRun(){const r=st().active;if(!r)return renderHub();if(r.items.some(x=>x.src==='bank')&&!bankReady())return withBank(showRun);renderRun();scrollTop()}
function renderRun(focusFeedback){
  const el=app(),cu=current();if(!el||!cu)return renderHub();
  const {r,item,a}=cu;if(!item){r.items.splice(r.i,1);if(!r.items.length){st().active=null;save();return renderHub()}r.i=Math.min(r.i,r.items.length-1);save();return renderRun()}
  chrome(runTitle(r));
  const isA=r.mode==='assess',ph=r.phase,ans=item.ans,o=r.items[r.i].o;
  const def=conceptDef(r.items[r.i].c||item.c);
  const optsHtml=o.map((orig,k)=>{
    const L=String.fromCharCode(65+k);let cls='',dis=false,mark='';
    if(isA){if(a.s1===orig)cls='sel'}
    else if(ph==='fb'){dis=true;if(orig===ans){cls='ok';mark='ถูก'}else if(orig===a.s1||orig===a.s2){cls='bad';mark='ผิด'}}
    else if(ph==='hint'){if(orig===a.s1){cls='bad crossed';dis=true;mark='ตัดออก'}}
    else if(ph==='conf'){dis=true;if(orig===a.s1)cls='sel'}
    const lab=ph==='fb'?optionLabel(item,orig):'';
    return `<button type="button" class="lh-opt ${cls}" ${dis?'disabled':''} aria-pressed="${(isA&&a.s1===orig)||(ph==='conf'&&a.s1===orig)?'true':'false'}" data-action="TGAT1Hub.pick" data-arg="${k}"><span class="lh-L">${L}</span><span class="lh-o" lang="en">${esc(item.opts[orig])}</span>${mark?`<span class="lh-mark">${mark}</span>`:''}${lab?`<small class="lh-form">${esc(lab)}</small>`:''}</button>`}).join('');
  const confHtml=(needConf(r)&&(ph==='conf'||(isA&&Number.isInteger(a.s1))))?`<div class="lh-conf" role="group" aria-label="ความมั่นใจในคำตอบนี้"><span>มั่นใจแค่ไหน?</span>${[['sure','มั่นใจ'],['some','ค่อนข้างมั่นใจ'],['not','ไม่มั่นใจ']].map(([v,t])=>`<button type="button" class="lh-chip ${a.cf===v?'on':''}" aria-pressed="${a.cf===v}" data-action="TGAT1Hub.conf" data-arg="${v}">${t}</button>`).join('')}</div>`:'';
  let fb='';
  if(!isA&&ph==='hint'){fb=`<div class="lh-hint" role="status"><b>ยังไม่ใช่ ลองคิดอีกครั้ง</b><p>${esc(item.hint||'ย้อนกลับไปดูโครงสร้างและคำสำคัญรอบช่องว่าง')}</p></div>`}
  if(!isA&&ph==='fb'){const ok=a.ok1||a.ok2;const wr=Array.isArray(item.wrong)?item.wrong:[];
    fb=`<div class="lh-fb ${a.ok1?'good':ok?'mid':'bad'}" role="status" tabindex="-1" id="lhFb"><b>${a.ok1?'ถูกต้อง':a.ok2?'ถูกในครั้งที่สอง':'ยังไม่ถูก'}</b>
      <p><b>ทำไมคำตอบนี้ถูก:</b> ${esc(item.why||'')}</p>
      ${wr.some(Boolean)?`<p><b>ทำไมตัวเลือกอื่นผิด:</b></p><ul>${o.map((orig,k)=>orig!==ans&&wr[orig]?`<li><b>${String.fromCharCode(65+k)}</b> ${esc(item.opts[orig])} — ${esc(wr[orig])}</li>`:'').join('')}</ul>`:''}
      ${r.items[r.i+1]&&r.items[r.i+1].rem&&!a.ok1?'<p class="lh-mini">ข้อต่อไปเป็นโจทย์ใหม่ในแนวคิดเดียวกัน ระดับง่ายลงเล็กน้อย</p>':''}
      ${a.cf&&!a.ok1&&a.cf==='sure'?'<p class="lh-mini">ตอบผิดทั้งที่มั่นใจ อาจเป็นความเข้าใจคลาดเคลื่อน ระบบจะนำแนวคิดนี้กลับมาทบทวนเร็วขึ้น</p>':''}
      ${a.cf&&a.ok1&&a.cf==='not'?'<p class="lh-mini">ถูกแต่ไม่มั่นใจ ระบบจะนำแนวคิดนี้กลับมาทบทวนอีกครั้ง</p>':''}</div>`}
  const canNext=isA?(Number.isInteger(a.s1)&&(!needConf(r)||a.cf)):ph==='fb';
  el.innerHTML=`<div class="lh-top"><button type="button" class="st-btn ghost small" data-action="TGAT1Hub.pause">พักไว้ก่อน (บันทึกแล้ว)</button><span class="lh-count">ข้อ ${r.i+1} / ${r.items.length}</span></div>
  <section class="st-card lh-q" aria-labelledby="lhQ">
    <div class="st-eyebrow">${esc(runTitle(r))} · ${esc(def.t||'')}</div>${bar((r.i)/r.items.length*100)}
    ${isA?'<p class="lh-mini">แบบทดสอบ: ไม่มีคำใบ้และจะเฉลยเมื่อทำครบทุกข้อ</p>':''}
    ${item.ctx?`<div class="lh-ctx" lang="en" tabindex="0" aria-label="บทอ่าน">${esc(item.ctx)}</div>`:''}
    <h2 id="lhQ" class="lh-stem" lang="en" tabindex="-1">${esc(item.stem)}</h2>
    <div class="lh-opts">${optsHtml}</div>${confHtml}${fb}
    <div class="lh-actions">${canNext?`<button type="button" class="st-btn" id="lhNext" data-action="TGAT1Hub.next">${r.i<r.items.length-1?'ข้อถัดไป →':(isA?'ส่งคำตอบและดูผล':'จบขั้นนี้')}</button>`:''}</div>
  </section>`;
  if(focusFeedback){const f=D.getElementById('lhFb')||D.getElementById('lhNext');if(f)try{f.scrollIntoView({block:'nearest'});if(f.id==='lhFb')f.focus({preventScroll:true})}catch(_){}}
}
function renderRunDone(mode,n,score,total){
  const el=app();const a=nextAction();
  el.innerHTML=`<section class="st-card lh-card" role="status"><div class="st-eyebrow">${esc({guided:'ฝึกพร้อมคำใบ้',practice:'ฝึกด้วยตนเอง',remed:'ซ่อมจุดอ่อน',review:'ทบทวนสะสม',extra:'ฝึกเพิ่ม'}[mode]||'')} เสร็จแล้ว</div>
   <h1 class="st-title">ตอบถูกตั้งแต่ครั้งแรก ${score}/${total}</h1>
   ${mode==='remed'?'<p class="lh-p">พร้อมทำแบบทดสอบท้ายหน่วยรอบใหม่แล้ว ระบบจะเลือกโจทย์ที่ยังไม่เคยใช้เท่าที่มี</p>':''}
   <div class="lh-actions"><button type="button" class="st-btn" data-action="TGAT1Hub.continue">เรียนต่อ: ${esc(describe(a))}</button><button type="button" class="st-btn ghost" data-action="TGAT1Hub.open">กลับ Learning Hub</button></div></section>`;scrollTop();
}
function renderAssessResult(rec,readonly){
  const el=app(),n=rec.u,us=unitState(n);chrome('ผลแบบทดสอบหน่วยที่ '+n);
  const wrongRows=Array.isArray(rec.wrong)?rec.wrong:[];
  el.innerHTML=`<section class="st-card lh-card"><div class="st-eyebrow">แบบทดสอบท้ายหน่วยที่ ${n}</div>
   <h1 class="st-title">${rec.k}/${rec.n} · ${rec.pct}% ${rec.pass?'· ผ่าน':'· ยังไม่ผ่าน'}</h1>
   <p class="lh-p">${rec.pass?(n<UNITS?'ปลดล็อกหน่วยที่ '+(n+1)+' แล้ว':'ผ่านครบทั้ง 70 หน่วย'):'เกณฑ์ผ่าน: ได้อย่างน้อย '+PASS_PCT+'% และทุกแนวคิดในหน่วยต้องถูกอย่างน้อยครึ่งหนึ่ง ระบบจะให้ซ่อมจุดอ่อนก่อนสอบรอบใหม่ด้วยโจทย์ชุดใหม่'}</p>
   <h2 class="lh-h">ผลรายแนวคิด</h2><ul class="lh-list">${Object.entries(rec.c||{}).map(([c,v])=>`<li><span>${esc(conceptDef(c).t)}</span><small>${v.k}/${v.t}${v.low?' · มีข้อที่ถูกแต่ไม่มั่นใจ (จะทบทวนเพิ่ม)':''}${(rec.weak||[]).includes(c)?' · ต้องซ่อม':''}</small></li>`).join('')}</ul>
   ${wrongRows.length?`<h2 class="lh-h">ทบทวนข้อที่ผิด</h2>${wrongRows.map(x=>`<div class="lh-example"><p lang="en">${esc(x.stem)}</p><p lang="en"><b>คุณตอบ:</b> ${esc(x.sel||'-')} · <b>คำตอบที่ถูก:</b> ${esc(x.ans)}</p><p>${esc(x.why)}</p></div>`).join('')}`:''}
   <div class="lh-actions">${readonly?'':`<button type="button" class="st-btn" data-action="TGAT1Hub.continue">${rec.pass?'เรียนต่อ':'เริ่มซ่อมจุดอ่อน'}</button>`}<button type="button" class="st-btn ghost" data-action="TGAT1Hub.open">กลับ Learning Hub</button></div></section>`;scrollTop();
}
function showErrors(){
  const el=app(),s=st();chrome('ความจำข้อผิดพลาด');
  const rows=Object.values(s.errors).filter(e=>e&&(e.wrong>0||e.type==='guess')).sort((a,b)=>(b.p||0)-(a.p||0)||(b.last||0)-(a.last||0)).slice(0,60);
  el.innerHTML=`<div class="lh-top"><button type="button" class="st-btn ghost small" data-action="TGAT1Hub.open">← Learning Hub</button></div>
  <section class="st-card lh-card"><div class="st-eyebrow">ERROR MEMORY</div><h1 class="st-title">ความจำข้อผิดพลาด</h1><p class="lh-p">ระบบจะไม่ถามข้อเดิมซ้ำ แต่จะนำแนวคิดเดียวกันกลับมาด้วยโจทย์ใหม่ตามรอบทบทวน</p>
  ${rows.length?`<ul class="lh-err">${rows.map(e=>{const r=s.concepts[e.c]||{};return `<li><div><b>${esc(conceptDef(e.c).t)}</b><small>${esc(TYPE_TH[e.type]||'')} · ผิด ${e.wrong}/${e.att} ครั้ง · ${esc(ST_TH[r.st]||'')} · ทบทวนครั้งถัดไป ${r.due?fmtDate(r.due):'-'}</small></div><p lang="en"><b>ตอบ:</b> ${esc(e.sel)} · <b>ที่ถูก:</b> ${esc(e.ans)}</p><p>${esc(e.why)}</p></li>`}).join('')}</ul>`:'<p class="lh-mini">ยังไม่มีข้อผิด</p>'}</section>`;scrollTop();
}

/* ------------------------------------------------------------------ integration with the existing app */
function updateBanner(){
  let el=D.getElementById('lhReturn');const s=HS;const show=!!(s&&(s.pending||s.returnTo))&&page()!=='hub';
  if(!show){if(el&&!el.hidden){el.hidden=true;D.body.classList.remove('lh-has-return')}return}
  if(!el){el=D.createElement('div');el.id='lhReturn';el.className='lh-return';el.setAttribute('role','region');el.setAttribute('aria-label','กลับไป Learning Hub');D.body.appendChild(el)}
  const html=`<span>${s.pending?'กิจกรรมจาก Learning Hub · หน่วยที่ '+s.pending.u:'บันทึกผลใน Learning Hub แล้ว'}</span><button type="button" data-action="TGAT1Hub.open">กลับ Learning Hub</button>`;
  if(el.dataset.h!==html){el.innerHTML=html;el.dataset.h=html}
  if(el.hidden!==false)el.hidden=false;D.body.classList.add('lh-has-return');
}
function homeCard(){
  const el=app();if(!el||page()!=='home'||!cur())return;const hero=el.querySelector('.dash-hero');if(!hero||el.querySelector('#lhHomeCard'))return;
  const s=st(),u=unitDef(s.unit),done=Object.values(s.units).filter(x=>x.st==='done').length,a=nextAction();
  hero.insertAdjacentHTML('afterend',`<section class="st-card lh-homecard" id="lhHomeCard" aria-labelledby="lhHomeT"><div><div class="st-eyebrow">LEARNING HUB · ${done}/${UNITS} หน่วย</div><h2 id="lhHomeT">หน่วยที่ ${s.unit} · ${esc(u?u.title:'')}</h2><p class="lh-mini">${esc(describe(a))}</p>${bar(done/UNITS*100)}</div><div class="lh-homecard-actions"><button type="button" class="st-btn" data-action="TGAT1Hub.continue">เรียนต่อ</button><button type="button" class="st-btn ghost small" data-action="TGAT1Hub.open">ดูเส้นทาง</button></div></section>`);
}
function analyticsCard(){
  const el=app();if(!el||page()!=='analytics'||!cur()||el.querySelector('#lhAnalytics'))return;
  const s=st(),done=Object.values(s.units).filter(x=>x.st==='done').length,con=Object.values(s.concepts).filter(r=>isObj(r)&&r.a>0),ms=con.filter(r=>r.st==='mastered').length,acc=s.stats.answered?Math.round(s.stats.correct/s.stats.answered*100):0;
  const head=el.firstElementChild;const html=`<section class="st-card lh-card" id="lhAnalytics" aria-labelledby="lhAnT"><div class="st-eyebrow">LEARNING HUB</div><h2 id="lhAnT">ความคืบหน้าในเส้นทาง 70 หน่วย</h2><div class="lh-kpis"><div><b>${done}/${UNITS}</b><small>หน่วยที่ผ่าน</small></div><div><b>${ms}</b><small>แนวคิดที่เชี่ยวชาญ</small></div><div><b>${s.stats.answered?acc+'%':'—'}</b><small>ความแม่นยำใน Hub (${s.stats.answered} ข้อ)</small></div><div><b>${dueConcepts().length}</b><small>ถึงรอบทบทวน</small></div></div><button type="button" class="st-btn ghost small" data-action="TGAT1Hub.open">เปิด Learning Hub</button></section>`;
  if(head)head.insertAdjacentHTML('afterend',html);else el.insertAdjacentHTML('afterbegin',html);
}
let wantContinue=false;
function render(){if(wantContinue){wantContinue=false;cont();return}renderHub()}
function continueToHub(){if(page()==='hub'){cont();return}let busy=false;try{busy=!!(VLT_RUN||Q)}catch(_){}const go=()=>{try{if(VLT_RUN){if(typeof W.VLT_stopTimer==='function')W.VLT_stopTimer();VLT_RUN=null}if(Q){if(typeof W.studioClearSession==='function')W.studioClearSession();if(typeof W.stopExamClock==='function')W.stopExamClock();Q=null}STUDIO_PAGE='hub';W.studioUpdateChrome('hub');cont()}catch(e){console.error('Learning Hub continue failed',e);renderHub()}};if(busy&&typeof W.TGConfirm==='function'){W.TGConfirm('กำลังทำแบบฝึกอยู่ หากไป Learning Hub ความคืบหน้ารอบนี้อาจไม่ถูกบันทึก ต้องการไปต่อหรือไม่?').then(ok=>{if(ok)go()}).catch(()=>{})}else go()}
function install(){
  if(typeof W.studioRender==='function'){const prev=W.studioRender;W.studioRender=function(){if(page()==='hub'){render();return}return prev.apply(this,arguments)}}
  if(typeof W.studioUpdateChrome==='function'){const prev=W.studioUpdateChrome;W.studioUpdateChrome=function(p){const out=prev.apply(this,arguments);if(p==='hub'){const c=D.getElementById('studioCrumb'),t=D.getElementById('studioTitle');if(c)c.textContent='LEARNING HUB';if(t)t.textContent='Learning Hub'}try{updateBanner()}catch(_){}return out}}
  if(typeof W.VLT_finish==='function'&&!W.VLT_finish.__hub){const prev=W.VLT_finish;const w=function(){let r=null;try{r=typeof VLT_RUN!=='undefined'?VLT_RUN:null}catch(_){}const out=prev.apply(this,arguments);try{onVltFinished(r)}catch(e){console.error('Learning Hub: VLT result not recorded',e)}return out};w.__hub=true;W.VLT_finish=w}
  if(typeof W.finish==='function'&&!W.finish.__hub){const prev=W.finish;const w=function(){let q=null;try{q=typeof Q!=='undefined'?Q:null}catch(_){}const out=prev.apply(this,arguments);try{onGameFinished(q)}catch(e){console.error('Learning Hub: game result not recorded',e)}return out};w.__hub=true;W.finish=w}
  if(typeof W.TGAT1_addHomeHook==='function')W.TGAT1_addHomeHook(()=>{try{homeCard()}catch(e){console.error(e)}});
  if(typeof W.TGAT1_addAnalyticsHook==='function')W.TGAT1_addAnalyticsHook(()=>{try{analyticsCard()}catch(e){console.error(e)}});
  W.addEventListener('storage',e=>{try{if(e&&e.key===KEY){HS=load();if(page()==='hub'&&!HS.active)renderHub()}}catch(err){console.warn('Learning Hub storage event ignored',err)}},{passive:true});
  try{homeCard()}catch(_){}
  updateBanner();
}

W.TGAT1Hub=Object.freeze({
  version:'1.0.0',schema:SCHEMA,key:KEY,
  open(){if(page()!=='hub'&&typeof W.studioNav==='function'){W.studioNav('hub');return}renderHub()},
  continue(){continueToHub()},
  step:(n,k)=>{try{STUDIO_PAGE='hub';W.studioUpdateChrome('hub')}catch(_){}stepEntry(n,k)},openUnit:n=>{try{STUDIO_PAGE='hub';W.studioUpdateChrome('hub')}catch(_){}openUnit(n)},
  learnDone,pick:pickOption,conf:setConf,next:nextQ,pause:pauseRun,fast:fastFinish,review:()=>{if(st().active){showRun();return}startReview()},extra:startExtra,
  showErrors,cancelPending,fullCoverage:startFullCoverage,coverage:coverageCount,
  logVocabulary(n,score,total){const s=st();const u=Number(n);if(!Number.isInteger(u)||u<1||u>UNITS)return false;log({k:'vocab',u,score:clamp(Number(score)||0,0,1000),total:clamp(Number(total)||0,0,1000),pct:Number(total)>0?Math.round(Number(score)/Number(total)*100):0});save();return true},
  // read-only helpers for diagnostics and automated tests
  state:()=>JSON.parse(JSON.stringify(st())),nextAction:()=>{const a=nextAction();return {k:a.k,u:a.u,step:a.step&&a.step.k}},
  family,conceptPool:(c)=>conceptPool(c).length,dueConcepts,reload:()=>{HS=load();return HS.unit},notice:()=>NOTICE,readonly:()=>READONLY,
  audit(){const c=cur();if(!c)return null;const x=idx();const out={units:c.units.length,items:x.items.size,problems:[]};
    c.units.forEach(u=>{if(!u.title||!u.learn||!(u.obj||[]).length)out.problems.push('unit '+u.n+': missing content');
      unitConcepts(u).forEach(cc=>{if(!x.concepts[cc])out.problems.push('unit '+u.n+': unknown concept '+cc);else if(bankReady()&&conceptPool(cc).length<4)out.problems.push('unit '+u.n+': small pool '+cc+' ('+conceptPool(cc).length+')')});
      if(u.guided&&Array.isArray(u.guided.ids))u.guided.ids.forEach(id=>{if(!x.items.has(id))out.problems.push('unit '+u.n+': missing item '+id)})});
    x.items.forEach(it=>{if(!Array.isArray(it.opts)||it.opts.length<3||!(it.ans>=0&&it.ans<it.opts.length))out.problems.push('item '+it.id+': bad options/answer');if(new Set(it.opts.map(o=>String(o).trim().toLowerCase())).size!==it.opts.length)out.problems.push('item '+it.id+': duplicate options');if(!x.concepts[it.c])out.problems.push('item '+it.id+': unknown concept '+it.c);if(!it.why)out.problems.push('item '+it.id+': no explanation')});
    return out}
});
install();
})();
