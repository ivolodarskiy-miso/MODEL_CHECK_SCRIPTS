#!/bin/csh

echo

cp /modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/ln2_${1}.csv LN2_${1}
cat /modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/zbr2_${1}.csv >> LN2_${1}

#
echo
echo "Processing LN2_${1} and ZBR2_${1} list..."

sed s/\'//g < LN2_${1} > LN2_NEW_${1}

cat LN2_NEW_${1} | awk -F, '{print $8,"$",$3,"$",$2,"$",$12}' | sort > LN2_temp_${1}

sed s/\ //g < LN2_temp_${1} > LN2_LIST_${1}

cat LN2_LIST_${1} | uniq > LN2_LIST_uniq_${1}


diff LN2_LIST_${1} LN2_LIST_uniq_${1} | awk -F "<" '{print $2}' | uniq | sort | uniq | uniq | grep $ > ln2_out_${1}.txt

cat ln2_out_${1}.txt

rm LN2_${1} LN2_NEW_${1} LN2_temp_${1} LN2_LIST_${1} LN2_LIST_uniq_${1}

echo
echo 
