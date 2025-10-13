# -*- coding: utf-8 -*-


#------------------------------------------------------------------------------
# Importation des bibliotheques et variables
#------------------------------------------------------------------------------

#-- Import de toute les definitions de variables et fonctions/ procedures a partir d'un autre fichier
#   RQ: le fichier "mon_fichier_de_variables.py" doit exister
#from mon_fichier_de_variables import *

#-- Import un objet à partir d'une bibliotheque
from datetime import datetime, date
from time import time, gmtime, strftime

#-- Import un objet 
import time as time2



#==============================================================================
#-- Fonction renvoyant la date / Heure systeme (datetime)
#==============================================================================
def Recuperer_DateHeure_Systeme():
    Result = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return(Result)
 
    
#==============================================================================
#-- Procedure : TTRAITEMENT 1 
#==============================================================================
def Lancer_Procedure_Traitement_1():
    print("Debut Traitement 1")
    print("Execution Traitement 1")
    print("Fin Traitement 1")


#==============================================================================
#-- Procedure : TTRAITEMENT 2
#==============================================================================
def Lancer_Procedure_Traitement_2():
    print("Debut Traitement 2")
    print("Execution Traitement 2")
    print("Fin Traitement 2")

  
#==============================================================================
#-- Procedure : TTRAITEMENT X
#==============================================================================
def Lancer_Procedure_Traitement_X(NumeroDeTraitement=0):
    myNumeroDeTraitement = str(NumeroDeTraitement)
    
    print("Debut Traitement " + myNumeroDeTraitement)
    print("Execution Traitement "+ myNumeroDeTraitement)
    print("Fin Traitement 2"+ myNumeroDeTraitement)




###############################################################################
# MAIN PROGRAM APPEL PAR SCRIPT DOS
###############################################################################
if __name__ == '__main__':
    

    #==========================================================================
    # DEBUT MAIN
	#==========================================================================
    print("=======================================================")    
    #-------------- DEBUT CHRONO
    MyBeginTimeSeconds = time2.time()
    print("\n\n")
    print("**** Debut du traitement en Secondes " + str(MyBeginTimeSeconds) + " ***")
	
	
   
    #--------------------------------------------------------------------------
    # Traitement 1 
    #--------------------------------------------------------------------------
    # print("Traitement 1")
    Lancer_Procedure_Traitement_1()
    print("-----------------------------------------\n")
   
    #--------------------------------------------------------------------------
    # Traitement 2
    #--------------------------------------------------------------------------
    Lancer_Procedure_Traitement_2()
    print("-----------------------------------------\n")

    #--------------------------------------------------------------------------
    # Traitement 3
    #--------------------------------------------------------------------------
    Lancer_Procedure_Traitement_X(3)
    print("-----------------------------------------\n")

        
        
	#==========================================================================
    # FIN MAIN
	#==========================================================================

    #-------------- FIN CHRONO 
    MyEndTimeSeconds = time2.time()
    print("**** Fin du traitement en Secondes " + str(MyEndTimeSeconds) + " ***")
    MyDeltaTimeSeconds = MyEndTimeSeconds - MyBeginTimeSeconds
    print("**** Duree du traitement en Secondes " + str(MyDeltaTimeSeconds) + " ***\n")
    print("\n")
    print("=======================================================")
