###############################################################################
#==============================================================================
#-- Parcourir un dossier et stocker les noms de fichiers dans une liste
#==============================================================================
#-- Import des bibliotheque
import sys, os, fnmatch

#-- Initialisation des variable
myListOfFile = []
myListOfFileTmp = []

myPathHtml = "C:/TD_DATALAKE\\DATALAKE/0_SOURCE_WEB"


#-- Recupere les noms longs  des fichiers dans le path
myListOfFileTmp = os.listdir(myPathHtml)



#-- Filtrer les fichiers concernés 
myPattern = "*INFO-EMP*.html"

#-- Parcour de tous les fichiers trouvés
for myEntry in myListOfFileTmp :  
    #-- On n'ajoute que les fichiers concernés
    if fnmatch.fnmatch(myEntry, myPattern)==True:
        myListOfFile.append(myEntry)

#-- Affichage du résultat
for i in myListOfFile : print("Ligne : " + i)


for myFileName in myListOfFile: print(myPathHtml + " --> " + str(myFileName))

#==============================================================================
###############################################################################

###############################################################################
#==============================================================================
#-- Copier des fichier d'une répertoir dans un autre
#==============================================================================
import shutil

for i in myListOfFile: print(i)

myPathHtmlIn = "C:/TD_DATALAKE/DATALAKE/0_SOURCE_WEB"
myPathHtmlOut = "C:/TD_DATALAKE\DATALAKE/1_LANDING_ZONE/LINKEDIN/EMP"

monPathFile_Test_IN = myPathHtmlIn + "/" + "13799-INFO-EMP-LINKEDIN-FR-1555991658.html"
monPathFile_Test_OUT = myPathHtmlOut + "/" + "monTest.html"

print(monPathFile_Test_IN)
print(monPathFile_Test_OUT)


shutil.copy(monPathFile_Test_IN, monPathFile_Test_OUT)

#--------------
for monNomDeFichier in myListOfFile: 
    print("Traitement :du fichier :", i)
    monPathFile_Test_IN = myPathHtmlIn + "/" + monNomDeFichier
    monPathFile_Test_OUT = myPathHtmlOut + "/" + monNomDeFichier
    print(monPathFile_Test_IN)
    print(monPathFile_Test_OUT)
    shutil.copy(monPathFile_Test_IN, monPathFile_Test_OUT)

###############################################################################