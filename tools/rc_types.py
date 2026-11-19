import re
def rc_type(p):
    p=p.lower()
    if re.search(r'most nearly mean|closest in meaning|as used in|word ',p): return 'vocab'
    if re.search(r'first|initial|begin|start|open|launch|before the others',p): return 'first-step'
    if re.search(r'infer|conclu|implied|imply|likely true|reasonably|interpretation|suggest',p): return 'inference'
    if re.search(r'why|purpose|reason|concern|problem|prompted',p): return 'purpose'
    return 'main-idea'
