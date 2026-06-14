# roblox checker v2.2.0

Mass username availability checker with last-online tracking.

## Features
- ✅ **Live table** — available names appear in real time during the check (Rich Live)
- 🔔 **Discord webhook** — every available name is sent instantly; a summary embed fires when the run finishes
- 🌐 Multi-language: English / Türkçe
- 📊 Export results: TXT or CSV

## Usage
```
python main.py
python main.py username1 username2
python main.py --file liste.txt
```

## Startup flow
1. Language select → 2. Theme select → 3. Webhook URL (optional) → 4. Input

## Webhook
Paste your Discord webhook URL at the prompt. Each available username triggers an
instant embed. A summary embed is sent at the end of the run.
Leave blank to skip.

## by kanhe
