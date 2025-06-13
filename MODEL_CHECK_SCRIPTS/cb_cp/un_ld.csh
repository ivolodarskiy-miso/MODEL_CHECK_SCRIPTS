#!/bin/csh

cat /modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/un_${1}.csv | awk -F "," '{print $1,","$2,","$5,","$12}' > ndonly_${1}.txt
cat /modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/ld_${1}.csv | awk -F "," '{print $1,","$2,","$5,","$18}' >> ndonly_${1}.txt
