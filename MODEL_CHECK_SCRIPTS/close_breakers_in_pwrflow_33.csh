#!/bin/csh


echo "please enter clone for pwrflow"
set clone = $<

setenv HABITAT_APPLICATION pwrflow
setenv HABITAT_FAMILY $clone

echo $HABITAT_APPLICATION
echo $HABITAT_FAMILY

tview stop PFSTUDY_PWRFLOW_${clone} -force

echo "p items;"         > p_options.rio

echo "/CBNORM = F;"    >> p_options.rio
echo "/CBCLOSE = T;"   >> p_options.rio
echo "/CBNOCH = F;"    >> p_options.rio
echo "/CLREMOVE = T;"  >> p_options.rio

echo "Setting the below power flow options:"
cat p_options.rio

hdbrio -i p_options.rio pwrflow > p_options.o

setenv PF_CMD_DEBUG TPALLNEW

# tview run PFSTUDY pwrflow ${clone}
pfstudy


## $HABUSER_BINDIR/custompwrflow top_closed

echo " We are done ... "

rm p_options.*


