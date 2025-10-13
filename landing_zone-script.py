import os
import shutil

# Dossier source
myPathSource = "TD_DATALAKE/DATALAKE/0_SOURCE_WEB"

# Dossiers cibles
path_linkedin_emp = "TD_DATALAKE/DATALAKE/1_LANDING_ZONE/LINKEDIN/EMP"
path_glassdoor_avi = "TD_DATALAKE/DATALAKE/1_LANDING_ZONE/GLASSDOOR/AVI"
path_glassdoor_soc = "TD_DATALAKE/DATALAKE/1_LANDING_ZONE/GLASSDOOR/SOC"

myListOfFileSourceTmp = os.listdir(myPathSource)

print("******** Début de copie des fichiers ********")

for myFileName in myListOfFileSourceTmp:
    src_file = os.path.join(myPathSource, myFileName)
    if "LINKEDIN" in myFileName:
        dst_dir = path_linkedin_emp
    elif "AVIS-SOC-GLASSDOOR" in myFileName:
        dst_dir = path_glassdoor_avi
    elif "INFO-SOC-GLASSDOOR" in myFileName:
        dst_dir = path_glassdoor_soc
    else:
        continue  

    dst_file = os.path.join(dst_dir, myFileName)

    print(f"Copie du fichier : {src_file} -- vers --> {dst_file}")

    shutil.copy(src_file, dst_file)

print("******** Fin de copie des fichiers ********")