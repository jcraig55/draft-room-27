#!/bin/bash
# Copies the rankings model (code, template, manual ranks, badge lists) into the GitHub repo's model/ folder.
R=/home/claude/draft-room-27/model
mkdir -p $R/fantasy $R/nfldata
cp /home/claude/fantasy/{proj.py,final.py,badges.py,top125.py,build_download.py,build_app.py,move.py,push_app.sh,sync_model.sh,template.html,top125.html,draft_order.json} $R/fantasy/
cp /home/claude/nfldata/{build.py,stats25.csv} $R/nfldata/
[ -f /home/claude/war-room-2027.html ] && cp /home/claude/war-room-2027.html $R/
cp /home/claude/fantasy/weekly_update.sh $R/ 2>/dev/null || true
cp /home/claude/fantasy/MODEL_README.md $R/README.md 2>/dev/null || true
# Data snapshot (exact current board, badges, Top 125) so this state can be restored even if stat sources change.
mkdir -p $R/snapshot
cp /home/claude/fantasy/{players.json,badges.json,breakouts.json,top125.json,proj.json} $R/snapshot/ 2>/dev/null || true
# Browser test scripts used to check the app
mkdir -p $R/tests && cp /home/claude/tests/{stream.js,live.js,timer2.js,press.js,fr.js,tt.js,grid.js,teams.js,simme.js,dock.js,pc.js,filt.js} $R/tests/ 2>/dev/null || true
