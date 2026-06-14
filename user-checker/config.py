#these lines are assisted by AI

APP_VER = "2.2.0"
APP_BY  = "kanhe"

UAPI  = "https://users.roblox.com/v1/usernames/users"
UDAPI = "https://users.roblox.com/v1/users/{uid}"
PAPI  = "https://presence.roblox.com/v1/presence/users"
FCAPI = "https://friends.roblox.com/v1/users/{uid}/friends/count"

TIMEOUT   = 12
BATCHSZ   = 100
WORKERS   = 20
PBATCH    = 50

STA = "available"
STT = "taken"
STI = "invalid"
STE = "error"

PLABELS = {0:"Offline",1:"Website",2:"In-Game",3:"Studio"}
PLABELS_TR = {0:"Çevrimdışı",1:"Web'de",2:"Oyunda",3:"Stüdyoda"}
PICONS  = {0:"💤",1:"🌐",2:"🎮",3:"🛠️"}

# ── Themes ────────────────────────────────────────────────────────────────
THEMES = {
    "1": {
        "name": "Red",
        "name_tr": "Kırmızı",
        "primary": "bold red",
        "secondary": "red",
        "accent": "bright_red",
        "available": "bold green",
        "taken": "bold red",
        "header": "bold red",
        "border": "red",
    },
    "2": {
        "name": "Blue",
        "name_tr": "Mavi",
        "primary": "bold blue",
        "secondary": "blue",
        "accent": "bright_blue",
        "available": "bold cyan",
        "taken": "bold blue",
        "header": "bold blue",
        "border": "blue",
    },
    "3": {
        "name": "Green",
        "name_tr": "Yeşil",
        "primary": "bold green",
        "secondary": "green",
        "accent": "bright_green",
        "available": "bold bright_green",
        "taken": "bold green",
        "header": "bold green",
        "border": "green",
    },
    "4": {
        "name": "Purple",
        "name_tr": "Mor",
        "primary": "bold magenta",
        "secondary": "magenta",
        "accent": "bright_magenta",
        "available": "bold green",
        "taken": "bold magenta",
        "header": "bold magenta",
        "border": "magenta",
    },
    "5": {
        "name": "Cyan",
        "name_tr": "Cyan",
        "primary": "bold cyan",
        "secondary": "cyan",
        "accent": "bright_cyan",
        "available": "bold bright_cyan",
        "taken": "bold cyan",
        "header": "bold cyan",
        "border": "cyan",
    },
    "6": {
        "name": "Yellow",
        "name_tr": "Sarı",
        "primary": "bold yellow",
        "secondary": "yellow",
        "accent": "bright_yellow",
        "available": "bold bright_yellow",
        "taken": "bold yellow",
        "header": "bold yellow",
        "border": "yellow",
    },
}

DEFAULT_THEME = THEMES["1"]

# Active theme — set at runtime by theme_select()
_active_theme = DEFAULT_THEME

def theme():
    return _active_theme

def set_theme(key):
    global _active_theme
    _active_theme = THEMES.get(key, DEFAULT_THEME)
