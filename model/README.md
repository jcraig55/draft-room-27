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

Draft order vs Top 125: `fantasy/draft_order.json` is the FROZEN draft board order (set Nov 13, 2026). Weekly updates must never regenerate or edit it. The app's draft (Board tab, pick window, computer drafters) uses it; the Top 125 tab and PDF use the live weekly rank. The two lists are customized separately: `python3 move.py --top "Name=N"` changes only the Top 125 (pins in proj.py), `--draft` changes only the frozen draft board (draft_order.json), `--both` changes both. The user's in-app moves are also separate (Top 125 tab ⇅ = Top 125 only, saved as dr27-topboard; draft-side ⇅ = draft board only, dr27-myboard).

WEEKLY UPDATE RULE (set Nov 16, 2026): weekly stat updates change ONLY the Top 125 "Player stats" page (and the stats columns in the Top 125 PDF).
- Frozen and never touched by weekly runs: `fantasy/draft_order.json` (draft board), `fantasy/top_order.json` (Top 125 rankings), and `fantasy/frozen/` (players, badges, breakouts used everywhere else in the app: draft side, bios, badges, pick window).
- The app gets this week's numbers through __LIVE__ (built from the live players.json/badges.json), used only by the Top 125 stats table.
- Orders change only via `move.py --top|--draft|--both` (when the user asks) or the user's in-app moves.
- The Player stats page has its OWN ranking: top 125 players by live 2026 PPR points per game (4+ games), rebuilt weekly from __LIVE__ rows. It is independent of the Top 125 board and the draft board.
