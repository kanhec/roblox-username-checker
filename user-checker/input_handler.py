import sys
from pathlib import Path
from rich.console import Console

c = Console()

def from_file(path, tr=False):
    p=Path(path)
    if not p.exists():
        c.print(f"[red]file not found: {path}[/red]" if not tr else f"[red]dosya bulunamadı: {path}[/red]")
        sys.exit(1)
    out=[]
    with p.open(encoding="utf-8") as f:
        for line in f:
            s=line.strip()
            if s and not s.startswith("#"): out.append(s)
    if not out:
        c.print("[yellow]file is empty[/yellow]" if not tr else "[yellow]dosya boş[/yellow]")
        sys.exit(0)
    return out

def prompt(tr=False):
    msg="enter usernames (comma/space/newline, empty line to finish):\n" if not tr else "kullanıcı adlarını gir (virgül/boşluk/satır, bitirmek için boş bırak):\n"
    c.print(f"[dim]{msg}[/dim]")
    lines=[]
    while True:
        try: line=input("  > ").strip()
        except (EOFError,KeyboardInterrupt): break
        if not line or line.lower() in("done","tamam","q","exit"): break
        lines.append(line)
    if not lines: return []
    raw=" ".join(lines)
    return [p.strip() for p in raw.replace(","," ").split() if p.strip()]

def get(args, tr=False):
    if "--file" in args:
        i=args.index("--file")
        if i+1>=len(args):
            c.print("[red]specify file path after --file[/red]")
            sys.exit(1)
        return from_file(args[i+1],tr)
    nf=[a for a in args if not a.startswith("-")]
    if nf:
        out=[]
        for a in nf: out.extend([p.strip() for p in a.split(",") if p.strip()])
        return out
    c.print()
    c.print(f"  [cyan]1[/cyan]  {'manual input' if not tr else 'manuel giriş'}")
    c.print(f"  [cyan]2[/cyan]  {'read from file (.txt)' if not tr else 'dosyadan oku (.txt)'}")
    c.print(f"  [cyan]q[/cyan]  {'exit' if not tr else 'çıkış'}")
    c.print()
    while True:
        ch=input("  > ").strip().lower()
        if ch in("1","2","q"): break
    if ch=="q": sys.exit(0)
    if ch=="2":
        path=input(("  file path: " if not tr else "  dosya yolu: ")).strip()
        return from_file(path,tr)
    return prompt(tr)
