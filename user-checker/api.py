from __future__ import annotations
import time, requests
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from config import UAPI,UDAPI,PAPI,FCAPI,TIMEOUT,BATCHSZ,PBATCH,PLABELS,PLABELS_TR,PICONS

_s = requests.Session()
_s.headers.update({"Content-Type":"application/json","Accept":"application/json","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

@dataclass
class Usr:
    username:str
    taken:bool=False
    uid:Optional[int]=None
    dname:Optional[str]=None
    desc:Optional[str]=None
    created:Optional[str]=None
    banned:bool=False
    ptype:Optional[int]=None
    loc:Optional[str]=None
    lastonline:Optional[str]=None
    fc:Optional[int]=None
    err:Optional[str]=None
    tr:bool=False

    def plabel(self):
        d = PLABELS_TR if self.tr else PLABELS
        return d.get(self.ptype,"?")
    def picon(self):
        return PICONS.get(self.ptype,"❓")
    def created_fmt(self):
        if not self.created: return None
        try:
            dt=datetime.fromisoformat(self.created.replace("Z","+00:00"))
            return dt.strftime("%d.%m.%Y")
        except: return self.created
    def lo_fmt(self):
        if not self.lastonline: return None
        try:
            dt=datetime.fromisoformat(self.lastonline.replace("Z","+00:00"))
            now=datetime.now(timezone.utc)
            s=int((now-dt).total_seconds())
            if s<60: return f"{s}s ago" if not self.tr else f"{s} sn önce"
            elif s<3600: return f"{s//60}m ago" if not self.tr else f"{s//60} dk önce"
            elif s<86400: return f"{s//3600}h ago" if not self.tr else f"{s//3600} sa önce"
            elif s<2592000: return f"{s//86400}d ago" if not self.tr else f"{s//86400} gün önce"
            else: return dt.strftime("%d.%m.%Y")
        except: return self.lastonline

def _post(url,data,retry=2):
    for i in range(retry+1):
        try:
            r=_s.post(url,json=data,timeout=TIMEOUT); r.raise_for_status(); return r.json()
        except requests.exceptions.HTTPError as e:
            if e.response and e.response.status_code==429: time.sleep(2+i*2); continue
            raise
        except requests.exceptions.Timeout:
            if i==retry: raise
            time.sleep(1)
    return None

def _get(url,retry=2):
    for i in range(retry+1):
        try:
            r=_s.get(url,timeout=TIMEOUT); r.raise_for_status(); return r.json()
        except requests.exceptions.HTTPError as e:
            if e.response and e.response.status_code==429: time.sleep(2+i*2); continue
            raise
        except requests.exceptions.Timeout:
            if i==retry: raise
            time.sleep(1)
    return None

def lookup(names):
    out={n.lower():None for n in names}
    for i in range(0,len(names),BATCHSZ):
        chunk=names[i:i+BATCHSZ]
        try:
            d=_post(UAPI,{"usernames":chunk,"excludeBannedUsers":False})
            if d and "data" in d:
                for e in d["data"]: out[e.get("requestedUsername","").lower()]=e
        except: pass
    return out

def detail(uid):
    try: return _get(UDAPI.format(uid=uid))
    except: return None

def presence(uids):
    pm={}
    for i in range(0,len(uids),PBATCH):
        chunk=uids[i:i+PBATCH]
        try:
            d=_post(PAPI,{"userIds":chunk})
            if d and "userPresences" in d:
                for p in d["userPresences"]:
                    if p.get("userId"): pm[p["userId"]]=p
        except: pass
    return pm

def full(names, tr=False):
    nm=lookup(names); res=[]; taken=[]
    for orig in names:
        inf=nm.get(orig.lower())
        if inf is None:
            res.append(Usr(username=orig,taken=False,tr=tr)); continue
        uid=inf.get("id")
        u=Usr(username=orig,taken=True,uid=uid,dname=inf.get("displayName"),tr=tr)
        res.append(u)
        if uid: taken.append((uid,u))
    if taken:
        pm=presence([x[0] for x in taken])
        for uid,u in taken:
            p=pm.get(uid,{})
            u.ptype=p.get("userPresenceType"); u.loc=p.get("lastLocation"); u.lastonline=p.get("lastOnline")
        for uid,u in taken:
            d=detail(uid)
            if d:
                u.desc=d.get("description"); u.created=d.get("created"); u.banned=d.get("isBanned",False)
    return res
