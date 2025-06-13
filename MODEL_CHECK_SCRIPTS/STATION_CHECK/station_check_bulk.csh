#!/bin/csh

sed s/\'//g < /modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/ln2_${1}.csv > LN2_NEW_${1}
sed s/\'//g < /modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/zbr2_${1}.csv > ZBR2_NEW_${1}

cat ST_NEW_${1}| awk -F, '{print  $3}' | sort | uniq > ST_LIST_${1}
cat LN2_NEW_${1}| awk -F, '{print  $3}' | sort | uniq > ST2_LIST_${1}
cat ZBR2_NEW_${1}| awk -F, '{print  $3}'| sort | uniq >> ST2_LIST_${1}
sed s/\ //g <ST2_LIST_${1}>ST2_LIST1_${1}
cat ST2_LIST1_${1} | sort | uniq > ST3_LIST_${1}

diff ST_LIST_${1} ST3_LIST_${1} | awk -F "<" '{print $2}'|sort | grep -v PSE_ >STATION_CHECK_${1}.txt

rm ST_LIST_${1} ST2_LIST_${1} ST2_LIST1_${1} ST3_LIST_${1} ST_NEW_${1} LN2_NEW_${1} ZBR2_NEW_${1}

cat STATION_CHECK_${1}.txt
