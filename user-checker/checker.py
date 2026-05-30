from __future__ import annotations
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Optional
from config import WORKERS
from validator import split
from api import full, Usr

class Res:
    def __init__(self):
        self.av=[];self.tk=[];self.inv={};self.err={}
        self._l=threading.Lock()
    def add_av(self,u):
        with self._l: self.av.append(u)
    def add_tk(self,u):
        with self._l: self.tk.append(u)
    def add_inv(self,u,r):
        with self._l: self.inv[u]=r
    def add_err(self,u,r):
        with self._l: self.err[u]=r
    @property
    def total(self): return len(self.av)+len(self.tk)+len(self.inv)+len(self.err)
    def tk_sorted(self):
        return sorted(self.tk, key=lambda r: r.lastonline or "", reverse=True)

def _chunk(chunk, res, cb, tr):
    try:
        for r in full(chunk,tr=tr):
            if r.taken: res.add_tk(r); cb and cb(r.username,"taken")
            else: res.add_av(r.username); cb and cb(r.username,"available")
    except Exception as e:
        for u in chunk: res.add_err(u,str(e)); cb and cb(u,"error")

def run(names, csz=25, workers=WORKERS, cb=None, tr=False):
    res=Res()
    ok,bad=split(names,tr=tr)
    for u,r in bad.items(): res.add_inv(u,r); cb and cb(u,"invalid")
    if not ok: return res
    chunks=[ok[i:i+csz] for i in range(0,len(ok),csz)]
    with ThreadPoolExecutor(max_workers=min(workers,len(chunks))) as pool:
        futs=[pool.submit(_chunk,c,res,cb,tr) for c in chunks]
        for f in as_completed(futs):
            try: f.result()
            except: pass
    return res
