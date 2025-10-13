#======================================================================================
#Eric KLOECKLE - v2
#Université Lumière Lyon 2 / Master 2  BI&A 
#« Business Intelligence & Analytics » / T.D.  DATALAKE « Gestion de données massives »
#======================================================================================


########################################################################################
# Outils 
########################################################################################
#------------------------------------------------------------------------------
#-- Afficher_une_ligne
#------------------------------------------------------------------------------
def Afficher_une_ligne(myCar = "-", nbCar=25):
    print(myCar*nbCar)
##--> Test de la fonction 
#Afficher_une_ligne()
##<--
    
    
#------------------------------------------------------------------------------
#-- Sauter_une_ligne
#------------------------------------------------------------------------------
def Sauter_une_ligne():
    print()
##--> Test de la fonction 
#Sauter_une_ligne()
##<--


#------------------------------------------------------------------------------
#-- Suppression du caractere "\n" (retour chariot) dans une chaine de caractere 
#   => Utilisation des "regular expression" - bibliotheque Python "re"
#------------------------------------------------------------------------------
import re
def Supprimer_SautDeLigne(myStr):
    myResult = ""
    print(re.sub(r'(.*)\\n','' r'\1', str(myStr)))
    return(myResult)
#========================================
##--> Test de la fonction 
#a = "toto \\n titi"
#print(a)    
#print(Supprimer_SautDeLigne(a))
##<--
 

########################################################################################
#    
# Exemple de passage de "Liste" vers "Fichier CSV" et inversement
#
########################################################################################

#==============================================================================
#==============================================================================
#  Passage d'une liste vers un CSV
#==============================================================================
#==============================================================================
#-- Chargement de la bibliotheque python pour la manipulation des fichiers CSV
import csv

#-- Création manuelle d'un jeux de test dans une liste
myListOfLineOut = [['Nom'   , 'Prenom', 'Age'],
                  ['Durant', 'Paul'  , '51' ],
                  ['Bruce' , 'Lee'   , '8'  ]]

#-- Visualisation du contenu de la liste de ligne à enregistrer dans un fichier 
Sauter_une_ligne()
Afficher_une_ligne()
for myLineOut in myListOfLineOut : print(myLineOut)
Afficher_une_ligne()

#-- Nom et Destination du fichier CSV à créer
myPathFileNameOut = "C:/TD_DATALAKE/DATALAKE/99_METADATA/testdata.csv"

#-- Ouverture du fichier en écriture
myFilePtrOut = open(myPathFileNameOut, "w", encoding="utf8", errors="ignore", newline='')

#-- Préparation de l'objet d'ecriture au format CSV
myWriterOut = csv.writer(myFilePtrOut, delimiter=';', quotechar='"',  quoting=csv.QUOTE_ALL, lineterminator='\n')

#-- Ecriture dans le ficheir du contenu de la liste
myWriterOut.writerows(myListOfLineOut)


#-- Fermeture du fichier 
myFilePtrOut .close()
#==============================================================================




#==============================================================================
#==============================================================================
#  Passage d'un un CSV vers une liste
#==============================================================================
#==============================================================================
#-- Chargement de la bibliotheque python pour la manipulation des fichiers CSV
import csv

#-- Initialisation des variables
myListOfLineIn = []

#-- Nom et Emplacement du fichier CSV à liste
myPathFileNameIn = "C:/TD_DATALAKE/DATALAKE/99_METADATA/testdata.csv"

#-- Ouverture du fichier en lecture
myFilePtrIn = open(myPathFileNameIn, "r", encoding="utf8", errors="ignore", newline='')

#-- Lecture du fichier CSV, segmentation des colonne, et stockage dans une liste 
myReaderIn = csv.reader(myFilePtrIn, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')

Sauter_une_ligne()
Afficher_une_ligne()
for myLineIn in myReaderIn : print(myLineIn)
Afficher_une_ligne()


myFilePtrIn.close()
#==============================================================================


