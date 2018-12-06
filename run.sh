#!/bin/bash

echo "[TENAX] loading data..."
if [ -d "CSIndex" ]; then
    (cd CSIndex;
     git pull
    )
else
    git clone https://github.com/aserg-ufmg/CSIndex.git    
fi

## installing python dependencies
echo "[TENAX] installing dependencies"
sudo -H pip3 install -r requirements.txt

DATA="/tmp/ranking.csv"
echo "[TENAX] generating data at ${DATA}"
python rank.py | sort -nr > ${DATA}

echo "[TENAX] generating plots at data directory"
## generate plots
plot() {
    # inputs
    LEVEL=${1}
    OUTFILENAME=${2}
    # tempo file
    TMPFILE="/tmp/scores"
    grep "$LEVEL" ${DATA} | awk '{print $1}' | cut -f1 -d, > "$TMPFILE"
    (cd R
     Rscript --vanilla genhistograms.R "$TMPFILE" "$LEVEL" "$OUTFILENAME" >/dev/null 2>&1
    )
}

plot "PQ-1A" pq1a
plot "PQ-1B" pq1b
plot "PQ-1C" pq1c
plot "PQ-1D" pq1d
plot "PQ-2" pq2
plot "\-\-" sembolsa

## generate grid with all plots
(cd R
 ./gengrid.R
)

## generating json
echo "[TENAX] generating json for website"
python csvtojson.py > web/data.json
