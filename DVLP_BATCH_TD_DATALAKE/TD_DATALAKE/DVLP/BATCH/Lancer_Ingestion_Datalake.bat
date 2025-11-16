@ECHO OFF
REM ***********************************************
REM      TRAITEMENT ALIMENTATION DATALAKE
REM          M2 BI&BD - Universite Lyon2 
REM          Cours G.D.M. - TD DATALAKE
REM                 2020/2021
REM ***********************************************

cls

echo ##############################################
echo #   DEBUT TRAITEMENT ALIMENTATION DATALAKE   #
echo ##############################################

echo ==============================================
echo *** 01-Acquisition_des_Donnees.bat
call 01-Acquisition_des_Donnees.bat
echo.
echo ==============================================
echo *** Extraction_Metadonnees
call 02-Extraction_Metadonnees.bat
echo.
echo ==============================================
echo *** Creation_Entrepot_de_donnees
call 03-Creation_Entrepot_de_donnees.bat
echo.
echo ==============================================
echo *** Preparation_Visualisation
call 04-Preparation_Visualisation.bat

echo ##############################################
echo #   FIN  TRAITEMENT ALIMENTATION DATALAKE    #
echo ##############################################
