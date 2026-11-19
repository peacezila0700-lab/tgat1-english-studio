import json,os,datetime
LOG=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'qa','changes_r3.jsonl')
def log(item_id,field,old,new,reason,category):
    with open(LOG,'a') as f: f.write(json.dumps({'id':item_id,'field':field,'old':old,'new':new,'reason':reason,'category':category},ensure_ascii=False)+'\n')
