import csv
from datetime import datetime
from pathlib import Path

def _ts(): return datetime.now().strftime("%Y%m%d_%H%M%S")

def to_txt(res, d=".", tr=False):
    f=Path(d)/f"results_{_ts()}.txt"
    ls=[f"roblox checker — {datetime.now().strftime('%d.%m.%Y %H:%M')}",""]
    if res.av:
        ls.append("=== AVAILABLE ===" if not tr else "=== MUSAİT ===")
        for u in sorted(res.av): ls.append(f"  {u}")
        ls.append("")
    if res.tk:
        ls.append("=== TAKEN ===" if not tr else "=== ALINMIŞ ===")
        for r in res.tk_sorted():
            ls.append(f"  {r.username:<20} id={r.uid or '?'}  {r.plabel()}  last={r.lo_fmt() or '?'}")
        ls.append("")
    if res.inv:
        ls.append("=== INVALID ===" if not tr else "=== GEÇERSİZ ===")
        for u,r in res.inv.items(): ls.append(f"  {u}: {r}")
        ls.append("")
    ls+=[f"total: {res.total}","available: "+str(len(res.av)),"taken: "+str(len(res.tk))]
    f.write_text("\n".join(ls),encoding="utf-8")
    return str(f)

def to_csv(res, d="."):
    f=Path(d)/f"results_{_ts()}.csv"
    with f.open("w",newline="",encoding="utf-8") as fp:
        w=csv.writer(fp)
        w.writerow(["username","status","user_id","display_name","presence","last_online","created","banned"])
        for u in res.av: w.writerow([u,"available","","","","","",""])
        for r in res.tk_sorted(): w.writerow([r.username,"taken",r.uid or "",r.dname or "",r.plabel(),r.lo_fmt() or "",r.created_fmt() or "","yes" if r.banned else "no"])
        for u in res.inv: w.writerow([u,"invalid","","","","","",""])
        for u in res.err: w.writerow([u,"error","","","","","",""])
    return str(f)
