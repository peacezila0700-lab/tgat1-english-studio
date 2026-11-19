"""Apply TC ambiguity fixes and regenerate item-specific Thai explanations (template-assisted)."""
import json,sys,os,re,collections,importlib.util
sys.path.insert(0,os.path.dirname(__file__));from changelog import log
spec=importlib.util.spec_from_file_location('f','content/tc_fixes_r3.py');F=importlib.util.module_from_spec(spec);spec.loader.exec_module(F)
V=json.load(open('data/vault.json'));by={q['id']:q for q in V}
qs=[q for q in V if q['kind']=='tc'];ctx=collections.OrderedDict()
for q in qs: ctx.setdefault(q['context'],[]).append(q)
groups=[ql for ql in ctx.values()]
for (pn,bn,old,new,opts,swap,why) in F.FIX:
    ql=groups[pn-1];q=ql[bn-1];assert f'({bn}) ____' in q['context'],(pn,bn)
    if old and new:
        assert old in q['context'],(pn,bn,old)
        c2=q['context'].replace(old,new)
        for x in ql:
            log(x['id'],'context',x['context'],c2,'TC fix (blank %d): %s'%(bn,why),'TC-ambiguity');x['context']=c2
    elif old: assert old in q['context'],(pn,bn,old)
    o=list(q['options']);key=o[q['answer']]
    if opts:
        pos=q['answer'];newo=list(opts[1:]);newo.insert(pos,opts[0]);assert len(set(newo))==4
        log(q['id'],'options',q['options'],newo,'TC fix: '+why,'TC-ambiguity');q['options']=newo
    if swap:
        a,b=swap;assert a in o and a!=key,(pn,bn,a,o);o[o.index(a)]=b
        log(q['id'],'options',q['options'],o,'TC fix: '+why,'TC-ambiguity');q['options']=o
# ---------- explanations
G={'before':'ก่อน','after':'หลังจาก','during':'ระหว่าง (ช่วงเวลา/เหตุการณ์)','until':'จนกระทั่ง','unless':'เว้นแต่/ถ้าไม่','although':'แม้ว่า','because':'เพราะ','therefore':'ดังนั้น (คำเชื่อมระหว่างประโยค)','if':'ถ้า','so':'ดังนั้น/เพื่อให้','so that':'เพื่อที่จะ','in order to':'เพื่อ (ตามด้วยกริยา)','in order':'เพื่อ (ต้องใช้ in order to/that)','while':'ขณะที่/ในขณะที่','whereas':'ในขณะที่ (เปรียบเทียบความต่าง)','who':'ผู้ซึ่ง (ใช้กับคน)','which':'ซึ่ง (ใช้กับสิ่งของ/ทั้งข้อความ)','where':'ที่ซึ่ง (สถานที่)','whose':'ของผู้/สิ่งที่ (แสดงความเป็นเจ้าของ)','when':'เมื่อ','what':'สิ่งที่','whether':'ว่า...หรือไม่','that':'ที่/ว่า','despite':'แม้จะมี (ตามด้วยคำนาม)','without':'โดยไม่','throughout':'ตลอดช่วง','once':'ทันทีที่/เมื่อ...แล้ว','whenever':'ทุกครั้งที่','whatever':'อะไรก็ตาม','whoever':'ใครก็ตาม','however':'อย่างไรก็ตาม/ไม่ว่าอย่างไร','as':'ในขณะที่/ตามที่/ในฐานะ','like':'เหมือน','than':'กว่า','instead of':'แทนที่จะ','because of':'เพราะ (ตามด้วยคำนาม)','in addition to':'นอกจาก...แล้ว','as well as':'รวมทั้ง','rather than':'แทนที่จะ','according to':'ตาม (สัดส่วน/ข้อมูล)','as soon as':'ทันทีที่','based on':'โดยอิงจาก','both':'ทั้ง...และ','either':'อย่างใดอย่างหนึ่ง (ใช้กับ or)','neither':'ไม่ทั้งสอง (ใช้กับ nor)','but':'แต่','and':'และ','or':'หรือ','every':'ทุก ๆ','any':'ใดก็ได้','all':'ทั้งหมด','even':'แม้แต่'}
PREP=set('at in on by for to with from of about through around among beside between across upon into over above along'.split())
REL=set('who which where whose what when whether that whenever whatever whoever however'.split())
def sentence(q):
    m=re.search(r'blank\s*\((\d+)\)',q['prompt']);n=m.group(1)
    hit=re.search(r'[^.!?]*\('+n+r'\)\s*_+[^.!?]*[.!?]?',q['context'])
    s=hit.group(0).strip()
    for k in range(1,9): s=s.replace(f'({k}) ____','____') if k!=int(n) else s
    return s, re.sub(r'\('+n+r'\)\s*_+','____',s)
def prevword(s):
    m=re.search(r"([A-Za-z’']+)\s+____",s);return m.group(1).lower() if m else ''
def nextword(s):
    m=re.search(r"____\s+([A-Za-z’']+)",s);return m.group(1).lower() if m else ''
MODAL=set('can could may might will would should must'.split())
def lemma_family(opts):
    base=min(opts,key=len).lower().replace('to ','')
    stem=base[:max(3,len(base)-3)]
    return all(o.lower().replace('to ','').startswith(stem[:4]) for o in opts)
def explain(q):
    o=q['options'];key=o[q['answer']];ds=[x for i,x in enumerate(o) if i!=q['answer']]
    raw,s=sentence(q);full=s.replace('____',key);pw,nw=prevword(s),nextword(s)
    head=f'ประโยคที่สมบูรณ์คือ “{full}”'
    lk=key.lower()
    if (q['id'] in OVR or lemma_family(o)) and lk not in G:
        # verb or word-form item
        if lk.startswith('to '): why=f'หลังกริยา {pw} ต้องใช้ to + กริยาช่องที่ 1 (to-infinitive)' if pw not in PREP else 'ต้องใช้ to + กริยาช่องที่ 1 เพื่อบอกจุดประสงค์'
        elif pw in MODAL: why=f'หลัง modal verb “{pw}” ต้องใช้กริยารูปฐาน (V1) ไม่เติม -s/-ed/-ing'
        elif pw=='to': why='หลัง to ในโครงสร้าง to-infinitive ต้องใช้กริยารูปฐาน (V1)'
        elif pw in('help','helps','let','make','makes'): why=f'โครงสร้าง {pw} + กรรม + กริยารูปฐาน จึงใช้ V1'
        elif lk.endswith('ly'): why='ช่องนี้ขยายกริยาหรือทั้งการกระทำ จึงต้องใช้คำกริยาวิเศษณ์ (adverb) ที่ลงท้าย -ly'
        elif lk.endswith('ing') and pw in PREP|{'by','without'}: why=f'หลังคำบุพบท “{pw}” ต้องใช้กริยาเติม -ing'
        elif lk.endswith('ed') and (pw.endswith('s') or pw in('the','library','editor','team','club')) or lk in('planned','began'): why='เล่าเหตุการณ์ที่เกิดขึ้นแล้วในอดีต และประโยครอบข้างใช้ past simple จึงต้องใช้กริยาช่องที่ 2'
        elif lk.endswith('s') and pw in('everyone','everybody','it','he','she'): why=f'ประธาน “{pw}” เป็นเอกพจน์ กริยาในปัจจุบันจึงต้องเติม -s'
        elif pw in('more','most','feel','be','become','keep','make','is','are','was','were','remain') or nw in('and','for','to'): why='ช่องนี้ต้องการคำคุณศัพท์ (adjective) มาขยายหรือเป็นส่วนเติมเต็มของประโยค'
        elif pw in('greater','with','of','the','a'): why='ช่องนี้อยู่ในตำแหน่งคำนาม จึงต้องใช้คำนาม (noun)'
        else: why='ช่องนี้ต้องการรูปคำที่ตรงกับหน้าที่ในประโยค (ชนิดของคำและรูปกริยา)'
        why=OVR.get(q['id'],why)
        rest='ตัวเลือก '+', '.join(ds)+' เป็นคำในตระกูลเดียวกันแต่เป็นชนิดคำหรือรูปกริยาที่ไม่เข้ากับตำแหน่งนี้'
        return f'{head} {why} {rest}'
    gk=G.get(lk);
    if lk in PREP: kind='คำบุพบท (preposition)';why=f'“{key}” เป็นคำบุพบทที่ใช้คู่กับคำรอบข้างได้ถูกต้องตามความหมายในประโยค (collocation)'
    elif lk in REL: kind='คำเชื่อม/คำนำอนุประโยค';why=f'“{key}” ({gk}) เชื่อมกับส่วนที่ตามมาได้ทั้งโครงสร้างและความหมาย'
    else: kind='คำเชื่อมหรือคำแสดงความสัมพันธ์';why=f'“{key}”'+(f' ({gk})' if gk else '')+' แสดงความสัมพันธ์ของความคิดในประโยคได้ตรงกับบริบท'
    dd=[]
    for d in ds:
        g=G.get(d.lower());dd.append(f'{d}'+(f' ({g})' if g else ''))
    rest='ส่วน '+', '.join(dd)+' ทำให้ประโยคผิดไวยากรณ์ ผิดการใช้คำร่วม หรือขัดกับความหมายของข้อความ'
    return f'{head} ช่องนี้ทดสอบ{kind} {why} {rest}'
OVR={'S01-Q036':'โครงสร้าง help + กรรม + กริยารูปฐาน (help the library share) จึงใช้ V1',
'S01-Q038':'โครงสร้าง ask + กรรม + to + V1 (asked the transit office to install)',
'S02-Q031':'to + V1 ใช้บอกจุดประสงค์ว่าเลือกวัตถุมาเพื่อสื่อความทรงจำ',
'S04-Q039':'based on เป็นวลีคงที่ แปลว่า “โดยอิงจาก” ตัวเลือกอื่นไม่ใช้กับ on ในความหมายนี้',
'S05-Q043':'ช่องนี้เป็นคำคุณศัพท์ที่ขยายคำนาม people จึงใช้ new',
'S11-Q038':'โครงสร้าง ask + กรรม + to + V1 (asked the group to mark)',
'S13-Q031':'to + V1 ใช้บอกจุดประสงค์ของการสร้างระบบชั้นวาง',
'S14-Q033':'to + V1 ใช้บอกจุดประสงค์ของการทำรายการจอง',
'S15-Q034':'informed เป็นคุณศัพท์ (participial adjective) ขยายคำนาม choices แปลว่า “ที่ตัดสินใจโดยมีข้อมูล”',
'S08-Q044':'ประธาน everyone เป็นเอกพจน์ กริยาในปัจจุบันจึงใช้ has',
'S18-Q038':'to + V1 ใช้บอกจุดประสงค์ของคำถาม (คำถามสั้น ๆ เพื่อเริ่มการอภิปราย)'}
TIP='อ่านทั้งประโยคและประโยคข้างเคียงก่อนเลือก ตรวจทั้งชนิดคำ/โครงสร้างไวยากรณ์ และความหมายที่เชื่อมกับเนื้อเรื่อง'
for q in qs:
    e=explain(q)
    if e!=q['explanation']: log(q['id'],'explanation',q['explanation'],e,'TC explanation regenerated in Thai with the completed sentence and a rule tied to the options (template-assisted, round 3)','TC-explanation');q['explanation']=e
    if q['tip']!=TIP: log(q['id'],'tip',q['tip'],TIP,'TC tip localized to Thai','TC-explanation');q['tip']=TIP
json.dump(V,open('data/vault.json','w'),ensure_ascii=False,indent=1)
print('ok',len(F.FIX))
