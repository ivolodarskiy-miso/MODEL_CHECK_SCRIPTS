import os
import sys
import csv
#record LD,ID_ST,ID_KV,I__ND_LD,ID_LD,I__BS_LD,LDAREA_LD,BASEW_LD,BASER_LD,PARFRACW_LD,PF_LD,ID_CO,I__MEAS_LD,WM_LD,MANUAL_LD,OPEN_LD,%SUBSCRIPT,ND,WMN,WMX,I__AREA,Z__AREA,ZST,RMX,RMN
#------0-----1-----2------3-------4-----5-----------6------7----------8----------9------10-----11--------12----13--------14------15-------16-----17--18--19----20-----21-----22--23--24
a = str(sys.argv[1])
#print (a,'\n')
file_name_1 = '/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/ld_'+ a +'.csv'
#print (file_name_1,'\n')
print ('\nChecking LDAREA\n')
#os.system ("hdbexport -d netmom -record LD -noprependpattern -pattern /modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/data_pattern.dat > ldarea.csv")
with open('ldarea_out.csv', mode='w') as write_outfile:
	write_outfile.write('ID_CO,ID_ST,ID_KV,ID_LD,LDAREA_LD\n')
	#with open("ldarea.csv",mode ='r') as f:
	with open(file_name_1,mode ='r') as f:
		csv_reader = csv.reader (f,delimiter=',')
		line_count = 0
		error_found = 0
		for row_ld in csv_reader:
			ld_co = (row_ld[11].strip()).replace("'","")
			ld_st = (row_ld[1].strip()).replace("'","")
			ld_kv = (row_ld[2].strip()).replace("'","")
			ld_id = (row_ld[4].strip()).replace("'","")
			ld_ldarea = (row_ld[6].strip()).replace("'","")
			#print (ld_co,ld_ldarea,"\n")
			if not(ld_ldarea.endswith("_C")) and not(ld_ldarea.endswith("_N")) : 
				if ((ld_co == "EMBA" and ld_ldarea != "EMILD") or 
					(ld_co == "EAI" and ld_ldarea != "EAILD") or 
					(ld_co == "EES" and (ld_ldarea != "ELILD" and ld_ldarea != "ETILD" and ld_ldarea != "NOPLD"))):
					ldarea_error = ld_co + "," + ld_st + "," + ld_kv + "," + ld_id + "," + ld_ldarea + "\n"
					write_outfile.write(ldarea_error)
					print ("CO = " + str(ld_co) + ", ST = " + str(ld_st) + ",KV = " + str(ld_kv) + ", Load id = " + str(ld_id) + ",LDAREA = " + str(ld_ldarea) + "\n")
					error_found +=1
				else :
					if ld_co != "EMBA" and ld_co != "EAI" and ld_co != "EES":
						ldarea_error = ld_co + "," + ld_st + "," + ld_kv + "," + ld_id + "," + ld_ldarea + "\n"
						write_outfile.write(ldarea_error)
						print ("CO = " + str(ld_co) + ", ST = " + str(ld_st) + ",KV = " + str(ld_kv) + ", Load id = " + str(ld_id) + ",LDAREA = " + str(ld_ldarea) + "\n")
						error_found +=1	
			line_count += 1
print ('Loads processed - ' + str(line_count) + '\n')
print ('Errors found - ' + str(error_found) + '\n')
 
