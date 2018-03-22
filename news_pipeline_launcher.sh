#!/bin/bash
cd news_pipeline

python3 news_monitor.py &
python3 news_fetcher.py & 
python3 news_deduper.py &

echo "=================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY

# for Mac OS to terminate python3 manually in terminal
# ps -ef | grep python3
# kill -9 XXXX