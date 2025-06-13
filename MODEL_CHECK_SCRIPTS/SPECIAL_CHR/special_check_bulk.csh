#!/bin/csh

echo ${1}
echo NETMOM_${1} > filename
# /chkspecialchar < NETMOM_${1} | grep name | awk '{print "p "$5"="$6"; /id="$7";"}'>invalid_charcater_${1}.csv
./chkspecialchar < filename | grep name | awk '{print "p "$5"="$6"; /id="$7";"}'>invalid_charcater_${1}.csv
cat invalid_charcater_${1}.csv
rm NETMOM_${1}
