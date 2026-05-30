import re

_P = re.compile(r'^[a-zA-Z0-9_]+$')

def chk(u):
    if not u: return False,"cant be empty"
    if len(u)<3: return False,f"min 3 chars (got {len(u)})"
    if len(u)>20: return False,f"max 20 chars (got {len(u)})"
    if not _P.match(u): return False,"invalid chars"
    if u[0]=='_' or u[-1]=='_': return False,"cant start/end with _"
    if '__' in u: return False,"no double underscore"
    return True,""

def chk_tr(u):
    if not u: return False,"boş olamaz"
    if len(u)<3: return False,f"min 3 karakter (şu an {len(u)})"
    if len(u)>20: return False,f"max 20 karakter (şu an {len(u)})"
    if not _P.match(u): return False,"geçersiz karakter"
    if u[0]=='_' or u[-1]=='_': return False,"_ ile başlayıp bitiremez"
    if '__' in u: return False,"çift alt çizgi olmaz"
    return True,""

def split(names, tr=False):
    ok,bad = [],{}
    fn = chk_tr if tr else chk
    for n in names:
        v,r = fn(n.strip())
        if v: ok.append(n.strip())
        else: bad[n.strip()] = r
    return ok,bad
