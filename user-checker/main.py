from __future__ import annotations
import sys, time
from rich.console import Console
from boot import splash, lang_select, webhook_setup
from display import all_results, LiveTable, c as dc
from input_handler import get
from checker import run
from exporter import to_txt, to_csv
import webhook as wh
import config

c = Console()


def _run_with_live(names, tr):
    """Run checker with real-time Live table and instant webhook delivery."""
    total = len(names)

    with LiveTable(total, tr) as live:
        def cb(username, status):
            live.tick(username, status)
            # Webhook: fire instantly for available names
            if status == "available" and wh.enabled():
                wh.send_available(username)

        t0  = time.time()
        res = run(names, cb=cb, tr=tr)

    elapsed = time.time() - t0
    return res, elapsed


def _export(res, tr):
    c.print()
    prompt = "  save results? [txt/csv/n]: " if not tr else "  sonuçları kaydet? [txt/csv/n]: "
    try:
        ch = input(prompt).strip().lower()
    except (EOFError, KeyboardInterrupt):
        return
    if ch == "txt":
        p = to_txt(res, tr=tr)
        c.print(f"\n  [green]saved:[/green] {p}")
    elif ch == "csv":
        p = to_csv(res)
        c.print(f"\n  [green]saved:[/green] {p}")
    else:
        c.print("  [dim]not saved.[/dim]" if not tr else "  [dim]kaydedilmedi.[/dim]")
    c.print()


def main():
    splash()
    tr   = lang_select()      # language + theme selection
    webhook_setup(tr)         # optional Discord webhook

    args  = sys.argv[1:]
    names = get(args, tr)

    if not names:
        c.print("[yellow]  no input.[/yellow]" if not tr else "[yellow]  giriş yok.[/yellow]")
        sys.exit(0)

    th = config.theme()
    c.print()
    c.print(
        f"  [{th['accent']}]"
        f"{'checking' if not tr else 'kontrol'} "
        f"{len(names)} "
        f"{'username(s)' if not tr else 'kullanıcı adı'}..."
        f"[/{th['accent']}]"
    )
    c.print()

    res, elapsed = _run_with_live(names, tr)

    # Send webhook summary
    if wh.enabled() and res.av:
        wh.send_summary(res.av, elapsed)

    all_results(res, elapsed, tr)
    _export(res, tr)

    while True:
        try:
            again = input(
                ("  check more? [y/n]: " if not tr else "  tekrar? [y/n]: ")
            ).strip().lower()
        except (EOFError, KeyboardInterrupt):
            break
        if again not in ("y", "e", "evet", "yes"):
            break
        names = get([], tr)
        if not names:
            break
        c.print()
        res, elapsed = _run_with_live(names, tr)
        if wh.enabled() and res.av:
            wh.send_summary(res.av, elapsed)
        all_results(res, elapsed, tr)
        _export(res, tr)

    c.print(
        "\n  [dim]bye.[/dim]\n" if not tr else "\n  [dim]görüşürüz.[/dim]\n"
    )


if __name__ == "__main__":
    main()
