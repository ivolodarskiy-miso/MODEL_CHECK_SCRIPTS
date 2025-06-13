#!/bin/sh -f

# Define color change and reset functions
set_red_text() {
  echo -ne "\033[91m"
}

set_yellow_text() {
  echo -ne "\033[33m"
}

reset_text_color() {
  echo -ne "\033[0m"
} 

_Date=`date +%m%d%G`
_time=`date +%H%M`

underscore=_
ROOTDIR=/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS
echo
echo "******Please make sure that the new netmom has been copied to power flow clone******"
echo 
echo "Please enter your clone"
read clone 
clone=`echo $clone |tr "[a-z]" "[A-Z]" `
echo "the clone is :${clone}"

arg_var=${_Date}:${_time}_${clone}

LOG_DIRECTORY=$ROOTDIR/run_checks_logs
LOG_FILE=$LOG_DIRECTORY/${_Date}_${_time}_${clone}.log
REDUCED_LOG_FILE=LOG_FILE=$LOG_DIRECTORY/${_Date}_${_time}_${clone}_reduced.log
mkdir -p "$(dirname "$LOG_FILE")"
: > "$LOG_FILE"
{
printf "Starting New Run Check ${_Date}:${_time}"

echo " Date is = $_Date "
echo " Time is = $_time "

echo " This will be passed as argument to all programs ---> $arg_var "
 

export HABITAT_APPLICATION=pwrflow
export HABITAT_FAMILY=$clone

echo "******context set to pwrflow $clone******" 
echo "Deleting files from: $ROOTDIR/OUTPUT"

find "$ROOTDIR/OUTPUT" -type f -exec rm -f {} +

cd ./data_pattern
csh -f ./dump_data_33_reduced.csh $arg_var

echo "_________________________________________________________________________________________________"
echo " Running Checks associated with HIGH Priority" 
echo "_________________________________________________________________________________________________" 

echo "_________________________________________________________________________________________________"
echo "set cb and cbtyp flag for CP"
cd ../cb_cp
set_red_text
python3 run_check_cb_cp_v2.py $arg_var  | sed 's/^/HIGH Priority: /'
mv cp_cb_${arg_var}.rio ../cleanup_rio/.
echo "Check ~/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/cleanup_rio/cp_cb_${arg_var}.rio"
reset_text_color
echo

echo "_________________________________________________________________________________________________"
echo "Running ZBRLOOP CHECK"
cd ../ZBRLOOP
set_red_text
# WARNING THIS FILE USES AN EXCEPTION LIST. If there appears to be something missing from the output check 
python3 zbrloopcheck_bulk.py $arg_var  | sed 's/^/HIGH Priority: /'
cp zbr_${arg_var}.log ../OUTPUT/zbr_${arg_var}.txt
reset_text_color
echo


echo "_________________________________________________________________________________________________"
echo "Running Script for checking if both ends of line are at same kv level"
echo "This is a low priority script but must be executed now in order to generate requisite files for other checks"
cd ../line_kv_level_RX 
python3 lines_kv_bulk.py $arg_var  | sed 's/^/LOW Priority: /' 
cat line_kv_${arg_var}.csv
mv line_kv_${arg_var}.csv ../OUTPUT/line_kv_${arg_var}.csv
echo

echo "_________________________________________________________________________________________________"
echo "Running Script for checking if line R/X is > 2"
cd ../line_kv_level_RX/
set_red_text
cat line_rx_${arg_var}.csv  | sed 's/^/HIGH Priority: /'
reset_text_color
mv line_rx_${arg_var}.csv ../OUTPUT/line_rx_${arg_var}.csv
echo


echo "_________________________________________________________________________________________________"
echo " Running Checks associated with Medium Priority" 
echo "_________________________________________________________________________________________________" 


echo "_________________________________________________________________________________________________" 
echo "Running check to verify if area definition matches file ~/AREA_UPDATE/area_flags_RTO.csv" 
cd ../area_check
set_yellow_text
python3 area_check_33.py $arg_var | sed 's/^/MEDIUM Priority: /'
reset_text_color

echo "_________________________________________________________________________________________________"
echo "Running check to verify if Monitored Elements in Exception list still exist in Netmom"
cd ../MONELEM
set_yellow_text
python3 monelm_exc_check.py $arg_var | sed 's/^/MEDIUM Priority: /'
cat invalid_elements_${arg_var}.csv
reset_text_color
mv invalid_elements_${arg_var}.csv ../OUTPUT/MONELEM_${arg_var}.txt
echo


echo "_________________________________________________________________________________________________"
echo "Running CO_LINE_CHECK"
cd ../CO_LINE_CHECK
set_yellow_text
python3 Line_check_bulk.py $arg_var | sed 's/^/MEDIUM Priority: /'
reset_text_color
mv CO_LINE_CHECK_${arg_var}.csv ../OUTPUT/CO_LINE_CHECK_${arg_var}.txt
echo

echo "_________________________________________________________________________________________________"
echo "Running script to check suspicious regsked"
cd ../DUPLICATE_LINE_CHECK
set_yellow_text
python3 checkregsk_bulk.py $arg_var | sed 's/^/MEDIUM Priority: /'
reset_text_color
mv suspicious_regsked_${arg_var}.txt ../OUTPUT/suspicious_regsked_${arg_var}.txt
echo

echo "_________________________________________________________________________________________________"
echo "Running Dangling equipment check"
cd ../DANGLE_NEW
set_yellow_text
python3 dangling_eq_bulk.py $arg_var | sed 's/^/MEDIUM Priority: /'
reset_text_color
mv new_dangling_equipments_${arg_var}.csv ../OUTPUT/new_dangling_equipments_${arg_var}.csv
echo


echo "_________________________________________________________________________________________________"
echo "check for XF where AVR = TRUE but regnd is null"
cd ../avr_regnd_check
set_yellow_text
python3 avr_regnd_bulk.py $arg_var | sed 's/^/MEDIUM Priority: /'
reset_text_color
mv avr_regnd_${arg_var}.csv ../OUTPUT/avr_regnd_${arg_var}.txt
echo 

echo "_________________________________________________________________________________________________"
echo "check for lines where Line DV is different from ST and ZST DV"
cd ../lines_in_wrong_dv
set_yellow_text
python3 line_in_wrong_dv_bulk.py $arg_var | sed 's/^/MEDIUM Priority: /'
mv lines_in_wrong_dv_${arg_var}.csv ../OUTPUT/lines_in_wrong_dv_${arg_var}.txt
reset_text_color
echo

echo "_________________________________________________________________________________________________"
echo "Load Wmn value check"
cd ../load_values
set_yellow_text
python3 loads.py $arg_var | sed 's/^/MEDIUM Priority: /'
mv rio_ld_${arg_var}.rio ../cleanup_rio/.
echo "Check ~/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/cleanup_rio/rio_ld_${arg_var}.rio"
reset_text_color
echo

echo "_________________________________________________________________________________________________"
echo "check for Childless cbtyp"
cd ../CBTYP_CHILDLESS
set_yellow_text
python3 childless_eq.py $arg_var | sed 's/^/MEDIUM Priority: /'
mv rem_cbtyp_childless_${arg_var}.rio ../cleanup_rio/.
echo "Check ~/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/cleanup_rio/rem_cbtyp_childless_${arg_var}.rio"
reset_text_color
echo

echo "_________________________________________________________________________________________________"
echo "check for CAP with mrnom = 0"
cd ../cpmrnom_0
set_yellow_text
python3 cp.py $arg_var | sed 's/^/MEDIUM Priority: /'
mv rio_cpmrnom_${arg_var}.rio ../cleanup_rio/.
echo "Check ~/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/cleanup_rio/rio_cpmrnom_${arg_var}.rio"
reset_text_color
echo



echo "_________________________________________________________________________________________________"
echo " Running Checks associated with LOW Priority" 
echo "_________________________________________________________________________________________________" 


echo "_________________________________________________________________________________________________"
echo "Running tieline_co_check CHECK"
cd ../tieline_co_check
python3 check_tln_bulk.py $arg_var | sed 's/^/LOW Priority: /'
mv tieline_co_check_$arg_var.txt ../OUTPUT/tieline_co_check_${arg_var}.txt
echo

echo "_________________________________________________________________________________________________"
echo "Running TLN_check"
cd ../TLN_CHECK
python3 TLN_check_bulk.py $arg_var | sed 's/^/LOW Priority: /'
mv TLN_check_${arg_var}.txt ../OUTPUT/TLN_check_${arg_var}.txt
echo

echo "_________________________________________________________________________________________________"
echo "Running Duplicate line name check"
cd ../DUPLICATE_LINE_CHECK
python3 uni_branch_name_bulk.py $arg_var | sed 's/^/LOW Priority: /'
mv DUPLICATE_LINE_CHECK_${arg_var}.txt ../OUTPUT/DUPLICATE_LINE_CHECK_${arg_var}.txt
echo

echo "_________________________________________________________________________________________________"
echo "Running Station check"
cd ../STATION_CHECK
python3 station_check_bulk.py $arg_var | sed 's/^/LOW Priority: /'
mv STATION_CHECK_${arg_var}.txt ../OUTPUT/STATION_CHECK_LINE_CHECK_${arg_var}.txt
echo

echo "_________________________________________________________________________________________________"
echo "Running Transformer Nominal KV check"
cd ../Nom_Kv_Check
python3 check_xf_bulk.py $arg_var | sed 's/^/LOW Priority: /'
mv Nominal_kv_${arg_var}.csv ../OUTPUT/Nominal_kv_${arg_var}.csv
echo

echo "_________________________________________________________________________________________________"
echo "Invalid character check"
cd ../SPECIAL_CHR
python3 special_char_check.py $arg_var | sed 's/^/LOW Priority: /'
mv invalid_charcater_${arg_var}.csv ../OUTPUT/invalid_charcater_${arg_var}.ecsv
echo 

echo "_________________________________________________________________________________________________"
echo "check for multiple line records with same name"
cd ../multiple_line_record_with_same_name
python3 multiple_line_record_with_same_name_bulk.py $arg_var | sed 's/^/LOW Priority: /'
mv multiple_line_record_with_same_name_${arg_var}.csv ../OUTPUT/multiple_line_record_with_same_name_${arg_var}.csv
echo

echo "_________________________________________________________________________________________________"
echo "check for Lines with same name at same node (LN2_CHECK)"
cd ../LN2_CHECK
csh -f ./ln2_check_bulk.csh $arg_var | sed 's/^/LOW Priority: /'
mv ln2_out_${arg_var}.txt ../OUTPUT/ln2_out_${arg_var}.txt
echo

echo "_________________________________________________________________________________________________"
echo "Unit regulation node check"
cd ../unit_regnd
python3 unit_regnd.py $arg_var | sed 's/^/LOW Priority: /'
mv rio_regnd_${arg_var}.rio ../cleanup_rio/.
mv unit_vtarget_${arg_var}.csv ../OUTPUT/unit_vtarget_${arg_var}.txt
mv unit_regnd_${arg_var}.csv ../OUTPUT/unit_regnd_${arg_var}.txt
echo "Check ~/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/cleanup_rio/rio_regnd_${arg_var}.rio"

echo "_________________________________________________________________________________________________"
echo "check for duplicate cb id in a station"
cd ../duplicate_cb_id
python3 duplicate_cb_id_bulk.py $arg_var | sed 's/^/LOW Priority: /'
mv duplicate_cb_id_${arg_var}.csv ../OUTPUT/duplicate_cb_id_${arg_var}.txt
echo

echo "_________________________________________________________________________________________________"
echo "Check for dead epnode"
cd ~/MODEL_SCRIPTS/FTR/deadepn
python3 run_check_dead_epnode.py $arg_var | sed 's/^/LOW Priority: /'



echo "_________________________________________________________________________________________________"
echo "Running Load area check"
cd ~/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/ldarea_chk
python3 ldarea_chk.py $arg_var | sed 's/^/LOW Priority: /'
echo


echo "_________________________________________________________________________________________________"
echo "Running unit rmx rmn wmx wmn mvarate genid checks"
cd ../unit_ratings_setting
python3 unit_ratings_setting.py $arg_var | sed 's/^/LOW Priority: /'
echo
echo

cd ../data_pattern
echo "_________________________________________________________________________________________________" 
echo "Running check to verify each LN, XF and ZB only have one LMT"
python3 ../DUPLICATE_LMT/duplicate_device_lmt.py lnlim_${arg_var}.csv xflim_${arg_var}.csv zblim_${arg_var}.csv  | sed 's/^/LOW Priority: /'

cd ~/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern
csh -f ./move_export_files.csh $arg_var


echo
echo
echo "Finished running check scripts. Please see the output files in" 
cd  ~/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/OUTPUT 
echo
echo
echo

} 2>&1 | tee -a "$LOG_FILE"
python3 reduce_runcheck_log.py --log_file "$LOG_FILE"