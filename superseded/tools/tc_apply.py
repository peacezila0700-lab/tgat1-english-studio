"""Apply round-3 TC edits and regenerate Thai explanations.
Hand-written 'why' text is used where provided; other items get rule-based explanations
(flagged in DATA-CHANGES as rule-generated, needing human review)."""
import json,sys,os,re,collections
sys.path.insert(0,os.path.dirname(__file__));from changelog import log
V=json.load(open('data/vault.json'));E=json.load(open('content/tc_r3_edits.json'))
tcs=[q for q in V if q['kind']=='tc'];groups=collections.OrderedDict()
for q in tcs: groups.setdefault(q['context'],[]).append(q)
G=list(groups.values())
HAND=set()
for ti,(tag,spec) in enumerate(sorted(E.items())):
    g=G[int(tag[1:])-1]
    ctx=g[0]['context']
    for old,new in spec.get('ctx',[]):
        assert old in ctx,(tag,old);ctx=ctx.replace(old,new)
    for q in g:
        if q['context']!=ctx: log(q['id'],'context',q['context'],ctx,'TC passage edited to remove answer ambiguity or an off-topic sentence copied from another passage','TC-fix');q['context']=ctx
    for n,it in spec.get('items',{}).items():
        q=g[int(n)-1];assert f'blank ({n})' in q['prompt']
        if 'options' in it:
            opts=[o for o in it['options'] if o!=it['key']];assert len(opts)==3,(tag,n)
            pos=q['answer'];opts.insert(pos,it['key'])
            if opts!=q['options']: log(q['id'],'options',q['options'],opts,'TC options changed: previous set had more than one defensible answer or a wrong key','TC-fix');q['options']=opts
        q['_why']=it['why'];HAND.add(q['id'])
# ---------- rule-based explanations
FW={'before':('both','ก่อน'),'after':('both','หลังจาก'),'until':('both','จนกว่า/จนถึง'),'during':('prep','ในระหว่าง'),'if':('conj','ถ้า'),'unless':('conj','เว้นแต่/ถ้าไม่'),
'although':('conj','แม้ว่า'),'because':('conj','เพราะ'),'so':('conj','ดังนั้น/เพื่อให้'),'so that':('conj','เพื่อให้'),'while':('conj','ขณะที่/ในขณะที่ (แสดงความต่าง)'),
'therefore':('adv','ดังนั้น (คำเชื่อมระหว่างประโยค ใช้หลังจุดหรืออัฒภาค)'),'when':('conj','เมื่อ'),'where':('rel','ที่ซึ่ง (สถานที่)'),'which':('rel','ซึ่ง (สิ่งของ/ทั้งประโยค)'),
'who':('rel','ผู้ซึ่ง (คน)'),'whose':('rel','ซึ่ง…ของ (ตามด้วยคำนาม)'),'that':('rel','ที่ (คนหรือสิ่ง)'),'what':('rel','สิ่งที่'),'whether':('conj','ว่า…หรือไม่'),'why':('conj','เหตุใด'),
'to':('prep','ไปยัง/เพื่อ (to + กริยา)'),'at':('prep','ที่/ณ (จุดเวลา สถานที่)'),'for':('prep','สำหรับ/เป็นเวลา'),'with':('prep','กับ/ด้วย'),'on':('prep','บน/ในวัน/เกี่ยวกับ'),
'in':('prep','ใน'),'through':('prep','ผ่าน/ทาง'),'from':('prep','จาก'),'by':('prep','โดย/ภายใน (กำหนดเวลา)'),'about':('prep','เกี่ยวกับ'),'among':('prep','ในหมู่ (มากกว่าสอง)'),
'between':('prep','ระหว่าง (สองฝ่าย)'),'around':('prep','รอบ ๆ'),'beside':('prep','ข้าง ๆ'),'across':('prep','ข้าม/ทั่ว'),'without':('prep','โดยไม่'),'despite':('prep','แม้จะมี'),
'instead of':('prep','แทนที่จะ'),'rather than':('prep','แทนที่จะ'),'according to':('prep','ตาม'),'based on':('prep','โดยอิงจาก'),'because of':('prep','เพราะ (ตามด้วยคำนาม)'),
'in addition to':('prep','นอกจาก…แล้ว'),'as well as':('prep','รวมทั้ง'),'as':('both','ขณะที่/ในฐานะ'),'like':('prep','เหมือน'),'than':('conj','กว่า'),'as soon as':('conj','ทันทีที่'),
'and':('coord','และ'),'but':('coord','แต่'),'or':('coord','หรือ'),'throughout':('prep','ตลอด'),'since':('both','ตั้งแต่/เนื่องจาก'),'whereas':('conj','ในขณะที่ (เปรียบต่าง)'),
'toward':('prep','ไปทาง'),'upon':('prep','บน/เมื่อ'),'of':('prep','ของ'),'among ':('prep','ในหมู่'),'every':('det','ทุก'),'all':('det','ทั้งหมด'),'each':('det','แต่ละ'),'some':('det','บาง'),
'a':('det','คำนำหน้านามเอกพจน์ (เสียงพยัญชนะ)'),'an':('det','คำนำหน้านามเอกพจน์ (เสียงสระ)'),'the':('det','คำนำหน้านามชี้เฉพาะ'),'—':('det','ไม่มีคำนำหน้านาม'),'much':('det','มาก (นามนับไม่ได้)'),
'most':('det','มากที่สุด'),'many':('det','มาก (นามนับได้)'),'more':('det','มากกว่า'),'less':('det','น้อยกว่า'),'least':('det','น้อยที่สุด'),'little':('det','น้อย (นามนับไม่ได้)'),'few':('det','น้อย (นามนับได้)')}
TYPE={'prep':'บุพบท (ตามด้วยคำนาม/วลีนาม หรือ V-ing)','conj':'คำเชื่อม (ตามด้วยประโยคที่มีประธานและกริยา)','both':'ใช้ได้ทั้งเป็นบุพบทและคำเชื่อม','rel':'คำนำอนุประโยค','coord':'คำเชื่อมที่เชื่อมคำหรือประโยคที่มีหน้าที่เท่ากัน','det':'คำกำหนดนาม','adv':'กริยาวิเศษณ์เชื่อมความ'}
ADJ={'clear','safe','simple','accessible','effective','informed','efficient','comfortable','new','careful','quick','calm','secure','meaningful','safer','calmer','simpler','newer','quicker','sufficient','informative','confident','comforting','careful'}
def pos(w):
    w=w.strip();lw=w.lower()
    if lw.startswith('to ') : return 'to + กริยา (infinitive)'
    if lw in ADJ or lw.endswith('er') and lw[:-2] in ADJ|{'saf','simpl'}: return 'คุณศัพท์ (adjective)'
    if lw.endswith('ly'): return 'กริยาวิเศษณ์ (adverb)'
    if re.search(r'(tion|sion|ity|ness|ment|ence|ance|ty|ure|ism)$',lw) or lw in {'care','access','basis','comfort','news','meaning','clarity','information','safety','security','confidence','calmness','quickness','effectiveness','efficiency'}: return 'คำนาม (noun)'
    if lw.endswith('ing'): return 'V-ing'
    if lw.endswith('ed') or lw in {'began','wrote','meant','been'}: return 'กริยาช่องที่ 2/3 (V2/V3)'
    if lw in {'is','has','be','being'}: return {'is':'กริยา be รูปปัจจุบันเอกพจน์','has':'กริยา have รูปเอกพจน์','be':'กริยา be รูปพื้นฐาน','being':'V-ing ของ be'}[lw]
    if lw.endswith('s') and not lw.endswith('ss'): return 'กริยาเติม -s (ประธานเอกพจน์)'
    return 'กริยารูปพื้นฐาน (base form)'
def is_family(opts):
    o=[x.lower() for x in opts if x!='—'];p=os.path.commonprefix(o)
    return len(p)>=3 or all(x.startswith('to ') or ' ' not in x for x in o) and len({x[:3] for x in o})==1
def around(q):
    m=re.search(r'([^.!?]*)\((\d+)\)\s*_+([^.!?]*[.!?]?)',q['context'][q['context'].find('('+re.search(r'blank \((\d+)\)',q['prompt']).group(1)+')')-400 if False else 0:])
    n=re.search(r'blank \((\d+)\)',q['prompt']).group(1)
    m=re.search(r'([^.!?]*)\('+n+r'\)\s*_+([^.!?]*[.!?]?)',q['context'])
    left=re.sub(r'\(\d+\)\s*_+','…',m.group(1)).strip();right=re.sub(r'\(\d+\)\s*_+','…',m.group(2)).strip()
    return left,right
VERBS=re.compile(r"\b(is|are|was|were|has|have|had|can|could|will|would|may|might|must|need|needs|ends|end|begins|begin|starts|start|opens|open|closes|arrive|arrives|feel|feels|agree|attend|attends|join|register|notice|see|find|request|requests|increases|grow|grows|learns|turns|changes|suits|complete|remain|remains|occur|return|returns|prefer|live|take|takes|asks|know|knows|enjoy|works|work|is|becomes|become|helps|help|matter|want|wants|seems|seem|reach|use|uses|appear|appears|stays|stay|happen|happens)\b",re.I)
TIME={'before','after','during','until','since','throughout'}
COND={'if','unless'};CONTRAST={'although','while','but','whereas'};CAUSE={'because','so','so that','therefore','as'}
REL={'who':'ใช้กับคน','which':'ใช้กับสิ่งของ','where':'ใช้กับสถานที่','whose':'ต้องตามด้วยคำนามที่แสดงความเป็นเจ้าของ','what':'หมายถึง “สิ่งที่” และไม่มีคำนามนำหน้า','that':'ใช้กับคนหรือสิ่งของ','when':'ใช้กับเวลา'}
def rule_exp(q):
    k=q['options'][q['answer']];left,right=around(q)
    lw=left.split()[-1] if left else '';rw=' '.join(right.split()[:4]).rstrip('.')
    others=[o for i,o in enumerate(q['options']) if i!=q['answer']]
    clause=bool(VERBS.search(' '.join(right.split()[1:8]))) and not right.lower().startswith(('the end','each','every'))
    if k.lower() in FW and not is_family(q['options']):
        kl=k.lower();t,g=FW[kl]
        if t in('conj','rel'): clause=True
        elif t=='prep': clause=False
        follow='ประโยค (มีประธานและกริยา)' if clause else 'คำนาม/วลีนาม'
        s=f"หลังช่องว่างคือ “{rw}…” ซึ่งเป็น{follow} คำตอบ {k} (‘{g}’) {'ใช้ได้ทั้งในฐานะบุพบทและคำเชื่อม' if t=='both' else 'เป็น'+TYPE[t]} และให้ความหมายตรงกับบริบท"
        bits=[]
        for o in others:
            ol=o.lower();ot,og=FW.get(ol,('?',''))
            if ot=='conj' and not clause: bits.append(f"{o} ต้องตามด้วยประโยค")
            elif ot=='prep' and clause: bits.append(f"{o} ต้องตามด้วยคำนาม ไม่ใช่ประโยค")
            elif ot=='adv': bits.append(f"{o} ใช้เชื่อมประโยคหลังจุดหรืออัฒภาค ไม่ใช้ในตำแหน่งนี้")
            elif ol in REL and kl in REL: bits.append(f"{o} {REL[ol]} จึงไม่ตรงกับคำที่อ้างถึง")
            elif ol in TIME and kl in TIME: bits.append(f"{o} (‘{og}’) ทำให้ลำดับเวลาไม่สอดคล้องกับเหตุการณ์")
            elif ol=='unless' and kl=='if': bits.append("unless (‘เว้นแต่’) ทำให้เงื่อนไขกลับความหมาย")
            elif ol in CONTRAST and kl not in CONTRAST: bits.append(f"{o} แสดงความขัดแย้ง ซึ่งไม่มีในประโยคนี้")
            elif ol in CAUSE and kl in CONTRAST: bits.append(f"{o} แสดงเหตุ/ผล แต่สองส่วนของประโยคขัดแย้งกัน")
            elif kl in CONTRAST and ol in COND: bits.append(f"{o} แสดงเงื่อนไข แต่ประโยคต้องการความขัดแย้ง")
            elif og: bits.append(f"{o} (‘{og}’) ไม่ให้ความหมายหรือการใช้คู่คำที่ประโยคนี้ต้องการ")
            else: bits.append(f"{o} ไม่เข้ากับโครงสร้างประโยค")
        return s+' ส่วน '+'; '.join(bits)
    p=pos(k);why=''
    if lw.lower() in {'can','could','may','might','must','should','will','would','to'} and 'base' in p: why=f'เพราะตามหลัง {lw} ซึ่งต้องใช้กริยารูปพื้นฐาน'
    elif 'V2' in p: why='เพราะประโยคเล่าเหตุการณ์ที่เกิดขึ้นแล้ว (อดีต) หรือเป็นรูป V3 ตามโครงสร้าง'
    elif 'adverb' in p: why='เพื่อขยายกริยาหรือการกระทำในประโยค'
    elif 'adjective' in p: why=f'เพื่อบอกลักษณะหลัง “{lw}” (เช่น become/feel/make + สิ่งที่ถูกขยาย + adjective หรือหน้าคำนาม)'
    elif 'infinitive' in p: why=f'เพราะ “{lw}” ตามด้วย to + กริยา'
    elif 'noun' in p: why=f'เพราะตำแหน่งนี้ต้องเป็นคำนามหลัง “{lw}”'
    elif '-s' in p: why='เพราะประธานเป็นเอกพจน์และเป็นปัจจุบันกาล'
    s=f"ช่องว่างหลัง “…{lw}” ต้องการ{p} {why} จึงใช้ {k}"
    bits=[f"{o} เป็น{pos(o)}" for o in others]
    return s+' ส่วน '+', '.join(bits)+' ซึ่งไม่ตรงกับหน้าที่ของคำในตำแหน่งนี้'
TIP='อ่านประโยคทั้งประโยคและประโยคถัดไปก่อนเลือก ตรวจทั้งชนิดคำ/โครงสร้าง (เช่น บุพบทต้องตามด้วยคำนาม คำเชื่อมต้องตามด้วยประโยค) และความหมายที่บริบทบังคับ'
for q in tcs:
    hand='_why' in q
    exp=q.pop('_why') if hand else rule_exp(q)
    if q['explanation']!=exp:
        log(q['id'],'explanation',q['explanation'],exp,'TC explanation rewritten in Thai: '+('hand-written for edited item' if hand else 'rule-generated from grammar category; replaces generic English boilerplate — needs human review'),'TC-explanation-hand' if hand else 'TC-explanation-rule');q['explanation']=exp
    if q['tip']!=TIP: log(q['id'],'tip',q['tip'],TIP,'TC tip localized to Thai','TC-tip');q['tip']=TIP
json.dump(V,open('data/vault.json','w'),ensure_ascii=False,indent=1)
print('hand',len(HAND),'rule',len(tcs)-len(HAND),collections.Counter(q['answer'] for q in tcs))
