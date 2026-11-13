#!/bin/bash
# Copies the rankings model (code, template, manual ranks, badge lists) into the GitHub repo's model/ folder.
R=/home/claude/draft-room-27/model
mkdir -p $R/fantasy $R/nfldata
cp /home/claude/fantasy/{proj.py,final.py,badges.py,top125.py,build_download.py,build_app.py,move.py,push_app.sh,sync_model.sh,template.html,top125.html} $R/fantasy/
cp /home/claude/nfldata/{build.py,stats25.csv} $R/nfldata/
[ -f /home/claude/war-room-2027.html ] && cp /home/claude/war-room-2027.html $R/
cp /home/claude/fantasy/weekly_update.sh $R/ 2>/dev/null || true
cp /home/claude/fantasy/MODEL_README.md $R/README.md 2>/dev/null || true
