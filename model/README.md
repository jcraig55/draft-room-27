# Draft Room ’27 — rankings model

This folder backs up everything behind the app: projection code, Jared's manual ranks, badge rules and hand-picked badges, and the page template. The app itself lives in the repo root (GitHub Pages).

## Where things are
- `fantasy/proj.py` — 2027 projection model. **Manual ranks** are the `OVR` (moved up) and `DOWN` (moved down) dictionaries near the bottom: player name → board rank.
- `fantasy/move.py` — list-style rank moves: `python3 move.py "Name=26" "Other Name=30"` (everyone else slides).
- `fantasy/badges.py` — badge rules plus hand-picked lists: `BREAKOUT`, `BUST_ADD`, `VOLATILE_ADD`, `CEILING_ADD`.
- `fantasy/template.html` — the Draft Room page (data placeholders filled at build time).
- `fantasy/top125.py`, `top125.html` — Top 125 list, Player stats page and PDF.
- `fantasy/build_download.py` → page build + app build (`build_app.py`, which copies the latest dated Top 125 PDF into the app as top125.pdf); `push_app.sh` publishes the app and syncs this folder.
- `nfldata/build.py` — turns nflverse CSVs into `raw.json`; `stats25.csv` is the 2025 season baseline.
- `war-room-2027.html` — the NFL mock draft (War Room ’27) source.

## Weekly refresh
1. Clone the repo to `/home/claude/draft-room-27`.
2. `bash /home/claude/draft-room-27/model/weekly_update.sh`
3. `/home/claude/fantasy/push_app.sh "Weekly stats update"`
4. The app is the single published version (Claude pages and dated HTML downloads are retired). Send the dated Top 125 PDF from `/home/claude/downloads` only if asked.


Badges (7): Safety pick, Volume machine, Breakout, High ceiling, Sleeper, Bust?, Volatile. badges.py guarantees every player gets at least one via fallback rules.

Draft order vs Top 125: `fantasy/draft_order.json` is the FROZEN draft board order (set Nov 13, 2026). Weekly updates must never regenerate or edit it. The app's draft (Board tab, pick window, computer drafters) uses it; the Top 125 tab and PDF use the live weekly rank. `move.py` applies the user's manual moves to BOTH lists.
