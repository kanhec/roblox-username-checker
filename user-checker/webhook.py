"""Discord webhook — müsait bulunan her isim anında gönderilir."""
from __future__ import annotations
import requests
from datetime import datetime

_session = requests.Session()
_session.headers.update({"Content-Type": "application/json"})

_url: str | None = None


def set_url(url: str | None):
    global _url
    _url = url.strip() if url and url.strip() else None


def get_url() -> str | None:
    return _url


def enabled() -> bool:
    return bool(_url)


def _ts() -> str:
    return datetime.utcnow().strftime("%d.%m.%Y %H:%M UTC")


def send_available(username: str) -> bool:
    """Tek müsait isim gönder. Başarı → True."""
    if not _url:
        return False
    payload = {
        "embeds": [
            {
                "title": "✅ Available Username",
                "description": f"```\n{username}\n```",
                "color": 0x57F287,
                "footer": {"text": f"roblox checker • {_ts()}"},
            }
        ]
    }
    try:
        r = _session.post(_url, json=payload, timeout=8)
        return r.status_code in (200, 204)
    except Exception:
        return False


def send_summary(av: list[str], elapsed: float) -> bool:
    """Kontrol bitince özet embed gönder."""
    if not _url or not av:
        return False
    names_str = "\n".join(sorted(av))
    payload = {
        "embeds": [
            {
                "title": f"📋 Check Complete — {len(av)} Available",
                "description": f"```\n{names_str}\n```",
                "color": 0x5865F2,
                "footer": {"text": f"roblox checker • {_ts()} • {elapsed:.2f}s"},
            }
        ]
    }
    try:
        r = _session.post(_url, json=payload, timeout=8)
        return r.status_code in (200, 204)
    except Exception:
        return False
