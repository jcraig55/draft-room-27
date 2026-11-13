# Draft Room ’27 — rankings model

This folder backs up everything behind the app: projection code, Jared's manual ranks, badge rules and hand-picked badges, and the page template. The app itself lives in the repo root (GitHub Pages).

## Where things are
- `fantasy/proj.py` — 2027 projection model. **Manual ranks** are the `OVR` (moved up) and `DOWN` (moved down) dictionaries near the bottom: player name → board rank.
- `fantasy/move.py` — list-style rank moves: `python3 move.py "Name=26" "Other Name=30"` (everyone else slides).
- `fantasy/badges.py` — badge rules plus hand-picked lists: `BREAKOUT`, `BUST_ADD`, `VOLATILE_ADD`, `CEILING_ADD`.
- `fantasy/template.html` — the Draft Room page (data placeholders filled at build time).
- `fantasy/top125.py`, `top125.html` — Top 125 list, Player stats page and PDF.
- `fantasy/build_download.py` → dated download + app build (`build_app.py`); `push_app.sh` publishes the app and syncs this folder.
- `nfldata/build.py` — turns nflverse CSVs into `raw.json`; `stats25.csv` is the 2025 season baseline.
- `war-room-2027.html` — the NFL mock draft (War Room ’27) source.

## Weekly refresh
1. Clone the repo to `/home/claude/draft-room-27`.
2. `bash /home/claude/draft-room-27/model/weekly_update.sh`
3. `/home/claude/fantasy/push_app.sh "Weekly stats update"`
4. Republish the Claude pages (Draft Room ’27: `/home/claude/fantasy/draft-room-2027.html` wrapped download; Top 125: `top125.html` + `stats.html`) and send the dated PDF/HTML from `/home/claude/downloads`.
