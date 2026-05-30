from __future__ import annotations
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.layout import Layout
from rich import box
import config

c = Console()


def _clr():
    os.system("cls" if os.name == "nt" else "clear")


def _pc(r):
    if r.ptype == 2:
        return f"[bold yellow]{r.picon()} {r.plabel()}[/bold yellow]"
    elif r.ptype in (1, 3):
        return f"[bold cyan]{r.picon()} {r.plabel()}[/bold cyan]"
    return f"[dim]{r.picon()} {r.plabel()}[/dim]"


def _lc(r):
    lo = r.lo_fmt()
    if not lo:
        return "[dim]-[/dim]"
    for w in ["s ago", "m ago", "sn", "dk", "секунд", "минут"]:
        if w in lo:
            return f"[bold green]{lo}[/bold green]"
    if "h ago" in lo or "sa" in lo:
        return f"[green]{lo}[/green]"
    if "d ago" in lo or "gün" in lo:
        return f"[yellow]{lo}[/yellow]"
    return f"[dim]{lo}[/dim]"


# ── Static result tables (shown after run) ────────────────────────────────

def taken_tbl(res, tr=False):
    th = config.theme()
    items = res.tk_sorted()
    if not items:
        return
    lbl = ("Taken Accounts" if not tr else "Alınmış Hesaplar") + f" ({len(items)})"
    t = Table(
        title=f"[{th['taken']}]{lbl}[/{th['taken']}]",
        box=box.MINIMAL_DOUBLE_HEAD,
        border_style="bright_black",
        header_style=th["taken"],
        show_lines=False,
        expand=True,
    )
    t.add_column("#", width=4, justify="right", style="dim")
    t.add_column("Username" if not tr else "Kullanıcı", min_width=16, style="bold white")
    t.add_column("Display", min_width=14, style="white")
    t.add_column("ID", min_width=10, style="dim cyan")
    t.add_column("Created" if not tr else "Kayıt", min_width=12)
    t.add_column("Status" if not tr else "Durum", min_width=14)
    t.add_column("Last Online" if not tr else "Son Aktif", min_width=16)
    t.add_column("Ban", width=5, justify="center")
    for i, r in enumerate(items, 1):
        ban = "[bold red]✓[/bold red]" if r.banned else "[dim]-[/dim]"
        t.add_row(
            str(i), r.username, r.dname or "-",
            str(r.uid) if r.uid else "-",
            r.created_fmt() or "-", _pc(r), _lc(r), ban,
        )
    c.print()
    c.print(t)


def av_tbl(res, tr=False):
    th = config.theme()
    if not res.av:
        return
    lbl = ("Available" if not tr else "Müsait") + f" ({len(res.av)})"
    t = Table(
        title=f"[{th['available']}]{lbl}[/{th['available']}]",
        box=box.MINIMAL_DOUBLE_HEAD,
        border_style="bright_black",
        header_style=th["available"],
        expand=True,
    )
    t.add_column("#", width=4, justify="right", style="dim")
    t.add_column(
        "Username" if not tr else "Kullanıcı Adı",
        style=th["available"], min_width=20,
    )
    t.add_column("Len" if not tr else "Uzunluk", width=6, justify="center", style="dim")
    for i, n in enumerate(sorted(res.av), 1):
        t.add_row(str(i), n, str(len(n)))
    c.print()
    c.print(t)


def inv_tbl(res, tr=False):
    if not res.inv:
        return
    lbl = ("Invalid" if not tr else "Geçersiz") + f" ({len(res.inv)})"
    t = Table(
        title=f"[bold yellow]{lbl}[/bold yellow]",
        box=box.MINIMAL,
        border_style="bright_black",
        header_style="bold yellow",
    )
    t.add_column("Username" if not tr else "Kullanıcı", style="yellow")
    t.add_column("Reason" if not tr else "Sebep", style="dim yellow")
    for n, r in res.inv.items():
        t.add_row(n, r)
    c.print()
    c.print(t)


def err_tbl(res, tr=False):
    if not res.err:
        return
    lbl = ("Errors" if not tr else "Hatalar") + f" ({len(res.err)})"
    t = Table(
        title=f"[bold magenta]{lbl}[/bold magenta]",
        box=box.MINIMAL,
        border_style="bright_black",
        header_style="bold magenta",
    )
    t.add_column("Username" if not tr else "Kullanıcı", style="magenta")
    t.add_column("Error" if not tr else "Hata", style="dim magenta")
    for n, r in res.err.items():
        t.add_row(n, r)
    c.print()
    c.print(t)


def summary(res, elapsed, tr=False):
    th = config.theme()
    c.print()
    if tr:
        lines = [
            f"[green]Müsait  : {len(res.av)}[/green]",
            f"[{th['taken']}]Alınmış : {len(res.tk)}[/{th['taken']}]",
            "[yellow]Geçersiz: " + str(len(res.inv)) + "[/yellow]",
            "[magenta]Hata    : " + str(len(res.err)) + "[/magenta]",
            f"[white]Toplam  : {res.total}[/white]",
            f"[dim]Süre    : {elapsed:.2f}s[/dim]",
        ]
    else:
        lines = [
            f"[green]available: {len(res.av)}[/green]",
            f"[{th['taken']}]taken    : {len(res.tk)}[/{th['taken']}]",
            "[yellow]invalid  : " + str(len(res.inv)) + "[/yellow]",
            "[magenta]errors   : " + str(len(res.err)) + "[/magenta]",
            f"[white]total    : {res.total}[/white]",
            f"[dim]time     : {elapsed:.2f}s[/dim]",
        ]
    c.print(Panel(
        Text.from_markup("\n".join(lines)),
        box=box.MINIMAL,
        border_style="bright_black",
        padding=(0, 2),
    ))
    c.print()


def all_results(res, elapsed, tr=False):
    taken_tbl(res, tr)
    av_tbl(res, tr)
    inv_tbl(res, tr)
    err_tbl(res, tr)
    summary(res, elapsed, tr)


# ── Live table (updated in real-time while checking) ──────────────────────

def _build_live_table(av: list[str], taken_count: int, done: int, total: int,
                      tr: bool) -> Table:
    """Build the live-updating table shown during checking."""
    th = config.theme()
    pct = done / total if total else 0
    bar_w = 30
    filled = int(bar_w * pct)
    bar = "█" * filled + "░" * (bar_w - filled)

    title_str = (
        f"[{th['primary']}]{'kontrol ediliyor' if tr else 'checking'}[/{th['primary']}]"
        f"  [{th['accent']}]{bar}[/{th['accent']}]"
        f"  [dim]{done}/{total}[/dim]"
    )

    t = Table(
        title=title_str,
        box=box.MINIMAL_DOUBLE_HEAD,
        border_style="bright_black",
        header_style=th["available"],
        expand=True,
    )
    t.add_column("#", width=4, justify="right", style="dim")
    t.add_column(
        "✅ " + ("Available Usernames" if not tr else "Müsait Kullanıcı Adları"),
        style=th["available"],
        min_width=24,
    )
    t.add_column("Len" if not tr else "Uzunluk", width=6, justify="center", style="dim")

    for i, name in enumerate(sorted(av), 1):
        t.add_row(str(i), name, str(len(name)))

    if not av:
        placeholder = "scanning..." if not tr else "taranıyor..."
        t.add_row("", f"[dim]{placeholder}[/dim]", "")

    # Mini counter footer row
    footer = (
        f"[green]{len(av)} available[/green]"
        f"  [dim]taken: {taken_count}[/dim]"
    ) if not tr else (
        f"[green]{len(av)} müsait[/green]"
        f"  [dim]alınmış: {taken_count}[/dim]"
    )
    t.caption = footer
    return t


class LiveTable:
    """Context manager — wraps Rich Live for real-time table updates."""

    def __init__(self, total: int, tr: bool = False):
        self._total = total
        self._tr = tr
        self._av: list[str] = []
        self._taken = 0
        self._done = 0
        self._live = Live(
            self._render(),
            console=c,
            refresh_per_second=8,
            transient=False,
        )

    def _render(self):
        return _build_live_table(
            self._av, self._taken, self._done, self._total, self._tr
        )

    def __enter__(self):
        self._live.__enter__()
        return self

    def __exit__(self, *args):
        self._live.update(self._render())
        self._live.__exit__(*args)

    def tick(self, username: str, status: str):
        """Call from checker callback — thread-safe update."""
        self._done += 1
        if status == "available":
            self._av.append(username)
        elif status == "taken":
            self._taken += 1
        self._live.update(self._render())
