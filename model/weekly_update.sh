#!/bin/bash
# Weekly refresh: restore the model from the repo, pull the latest nflverse stats, rebuild everything.
# Run from anywhere after cloning jcraig55/draft-room-27 to /home/claude/draft-room-27.
set -e
REPO=/home/claude/draft-room-27
mkdir -p /home/claude/fantasy /home/claude/nfldata /home/claude/app /home/claude/downloads
cp -r $REPO/model/fantasy/. /home/claude/fantasy/
cp -r $REPO/model/nfldata/. /home/claude/nfldata/
cp $REPO/model/war-room-2027.html /home/claude/ 2>/dev/null || true
cp $REPO/model/weekly_update.sh $REPO/model/README.md /home/claude/fantasy/ 2>/dev/null || true
mv /home/claude/fantasy/README.md /home/claude/fantasy/MODEL_README.md 2>/dev/null || true
cp $REPO/*.png /home/claude/app/
chmod +x /home/claude/fantasy/*.sh
cd /home/claude/nfldata
B=https://github.com/nflverse/nflverse-data/releases/download
curl -sSfL -o stats26.csv $B/stats_player/stats_player_week_2026.csv
curl -sSfL -o snaps26.csv $B/snap_counts/snap_counts_2026.csv
curl -sSfL -o players.csv $B/players/players.csv
echo "Stats through week: $(python3 -c "import pandas as p;print(int(p.read_csv('stats26.csv',usecols=['week']).week.max()))")"
python3 build.py
cd /home/claude/fantasy
python3 final.py
python3 build_download.py
echo "Rebuilt. Next: push_app.sh (the app is the only published version)."
