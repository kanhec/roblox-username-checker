from __future__ import annotations
import time, random, os, sys
import pyfiglet
from rich.console import Console
from rich.text import Text
from rich.align import Align
from rich import box

import config
import webhook as wh

def _print_art(con, text, style):
    for line in text.splitlines():
        con.print(Align.center(Text(line, style=style)))

c = Console()

_MSGS = [
    "initializing modules...",
    "loading config...",
    "setting up thread pool...",
    "connecting to roblox endpoints...",
    "checking rate limits...",
    "preparing validator...",
    "cache cleared.",
    "ready.",
]

_MSGS_TR = [
    "modüller yükleniyor...",
    "ayarlar okunuyor...",
    "thread havuzu hazırlanıyor...",
    "roblox uç noktalarına bağlanılıyor...",
    "rate limit kontrolü...",
    "doğrulayıcı hazırlanıyor...",
    "önbellek temizlendi.",
    "hazır.",
]


def _clr():
    os.system("cls" if os.name == "nt" else "clear")


def _bar(pct, width=36):
    filled = int(width * pct)
    bar = "█" * filled + "░" * (width - filled)
    return bar


def _star_field(seed=0):
    random.seed(seed)
    lines = []
    chars = ["*", "·", "˖", "✦", "✧", "⋆", "°"]
    for _ in range(6):
        row = ""
        for _ in range(72):
            if random.random() < 0.07:
                row += random.choice(chars)
            else:
                row += " "
        lines.append(row)
    return "\n".join(lines)


def splash():
    _clr()
    title_art = pyfiglet.figlet_format("ROBLOX", font="big")
    sub_art   = pyfiglet.figlet_format("CHECKER", font="small")
    th = config.theme()

    for frame in range(3):
        _clr()
        sf = _star_field(frame)
        c.print(Text(sf, style="bright_black"))
        c.print()
        _print_art(c, title_art, th["primary"])
        c.print()
        _print_art(c, sub_art, th["secondary"])
        c.print()
        c.print(Align.center(Text(
            "mass username checker · last-online tracker · by kanhe",
            style="dim"
        )))
        time.sleep(0.18)

    c.print()


def loading(tr=False):
    msgs  = _MSGS_TR if tr else _MSGS
    total = len(msgs)
    th    = config.theme()
    c.print()
    for i, msg in enumerate(msgs):
        pct     = (i + 1) / total
        bar     = _bar(pct)
        pct_str = f"{int(pct*100):3d}%"
        c.print(
            f"\r  [dim]{bar}[/dim] [{th['accent']}]{pct_str}[/{th['accent']}]"
            f"  [dim white]{msg}[/dim white]",
            end=""
        )
        time.sleep(random.uniform(0.08, 0.22))
    c.print()
    c.print()


# thewwmes

def theme_select(tr=False):
    _clr()
    title_art = pyfiglet.figlet_format("ROBLOX", font="big")
    sub_art   = pyfiglet.figlet_format("CHECKER", font="small")
    sf = _star_field(42)

    c.print(Text(sf, style="bright_black"))
    c.print()
    _print_art(c, title_art, "bold red")
    _print_art(c, sub_art, "red")
    c.print()

    label = "select color theme / renk teması seç" if not tr else "renk teması seç"
    c.print(Align.center(Text(label, style="dim")))
    c.print()

    color_map = {
        "1": "bold red",
        "2": "bold blue",
        "3": "bold green",
        "4": "bold magenta",
        "5": "bold cyan",
        "6": "bold yellow",
    }
    for key, th in config.THEMES.items():
        name = th["name_tr"] if tr else th["name"]
        style = color_map[key]
        c.print(Align.center(Text(f"  {key}  {name}", style=style)))

    c.print()
    while True:
        try:
            ch = input("  > ").strip()
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)
        if ch in config.THEMES:
            break

    config.set_theme(ch)


#, langs
def lang_select():
    _clr()
    title_art = pyfiglet.figlet_format("ROBLOX", font="big")
    sub_art   = pyfiglet.figlet_format("CHECKER", font="small")
    sf = _star_field(99)

    c.print(Text(sf, style="bright_black"))
    c.print()
    _print_art(c, title_art, "bold red")
    _print_art(c, sub_art, "red")
    c.print()
    c.print(Align.center(Text("select language / dil seç", style="dim")))
    c.print()
    c.print(Align.center(Text("  1  English", style="cyan")))
    c.print(Align.center(Text("  2  Türkçe",  style="cyan")))
    c.print()

    while True:
        try:
            ch = input("  > ").strip()
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)
        if ch in ("1", "2"):
            break

    tr = ch == "2"

   
    theme_select(tr)

    _clr()
    th = config.theme()
    _print_art(c, title_art, th["primary"])
    _print_art(c, sub_art, th["secondary"])
    c.print()
    loading(tr)
    return tr


# Webhook

def webhook_setup(tr=False):
    """Prompt user for optional Discord webhook URL."""
    th = config.theme()
    c.print()
    if tr:
        c.print(f"  [{th['accent']}]Discord webhook URL gir (atlamak için boş bırak):[/{th['accent']}]")
    else:
        c.print(f"  [{th['accent']}]Enter Discord webhook URL (leave empty to skip):[/{th['accent']}]")
    c.print()
    try:
        url = input("  > ").strip()
    except (EOFError, KeyboardInterrupt):
        return
    if url:
        wh.set_url(url)
        ok_msg = "webhook ayarlandı ✓" if tr else "webhook set ✓"
        c.print(f"\n  [bold green]{ok_msg}[/bold green]")
    else:
        skip_msg = "webhook atlandı." if tr else "webhook skipped."
        c.print(f"\n  [dim]{skip_msg}[/dim]")
    c.print()
