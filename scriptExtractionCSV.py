import pandas as pd
from bs4 import BeautifulSoup
import os

# ============================================================
# === PHASE 2 - EXTRACTION : Lecture du CSV et affichage des fichiers HTML
# ============================================================

# -- Chemin vers le fichier de métadonnées techniques
metadata_path = "C:\\TD_DATALAKE\\projet-datalake\\TD_DATALAKE\\DATALAKE\\99_METADATA\\metadata_technique.csv"

# -- Lecture du CSV avec séparateur point-virgule
metadata = pd.read_csv(metadata_path, sep=';', quotechar='"')

print("Fichier de métadonnées chargé avec succès.\n")

# -- Regroupement des lignes par clé unique
grouped = metadata.groupby("cle_unique")


#==============================================================================
#-- LINKEDIN (EMPLOI) : Libellé de l'offre
#==============================================================================
def extraire_libelle_emploi_EMP(objet_html):
    texte_tmp = objet_html.find_all('h1', attrs = {'class':'topcard__title'}) 
    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp[0].text)
        if (texte_tmp == []) : 
            resultat = 'NULL'
        else:
            resultat = texte_tmp
    return(resultat)


#==============================================================================
#-- LINKEDIN (EMPLOI) : Nom de la Société demandeuse
#==============================================================================
def extraire_nom_entreprise_EMP(objet_html):
    texte_tmp = objet_html.find_all('span', attrs = {'class':'topcard__flavor'}) 
    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp[0].text)
        if (texte_tmp == []) : 
            resultat = 'NULL'
        else:
            resultat = texte_tmp
    return(resultat)


#==============================================================================
#-- LINKEDIN (EMPLOI) : Ville de l'emploi proposé
#==============================================================================
def extraire_ville_emploi_EMP (objet_html):
    texte_tmp = objet_html.find_all('span', attrs = {'class':'topcard__flavor topcard__flavor--bullet'}) 
    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp[0].text)
        if (texte_tmp == []) : 
            resultat = 'NULL'
        else:
            resultat = texte_tmp
    return(resultat)


#==============================================================================
#-- LINKEDIN (EMPLOI) : Texte de l'offre d'emploi
#==============================================================================
def extraire_texte_emploi_EMP (objet_html):
    texte_tmp = objet_html.find_all('div', attrs = {"class": "description__text description__text--rich"})
    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp[0].text)
        if (texte_tmp == []) : 
            resultat = 'NULL'
        else:
            resultat = texte_tmp
    return(resultat)


# ============================================================
# === PARCOURS DES FICHIERS HTML ET EXTRACTION DES DONNÉES
# ============================================================

# Liste pour stocker les résultats
donnees_extraites = []

for cle, group in grouped:
    dico = dict(zip(group["colonne"], group["valeur"]))
    localisation = dico.get("localisation_du_fichier_html", "NON TROUVÉE")
    nom_fichier = dico.get("nom_du_fichier_html", "NON TROUVÉ")

    # On ne garde que les fichiers LINKEDIN/EMP
    if "LINKEDIN/EMP" not in localisation.upper():
        continue

    chemin_complet = os.path.join("C:\\TD_DATALAKE\\projet-datalake", localisation.replace("/", "\\"))

    print(f"\nClé unique : {cle}")
    print(f"Nom du fichier : {nom_fichier}")
    print(f"Localisation complète : {chemin_complet}")
    print("-" * 80)

    try:
        # Lecture du fichier HTML
        with open(chemin_complet, "r", encoding="utf-8") as f:
            contenu_html = f.read()

        # Création du parser HTML
        objet_parser_html = BeautifulSoup(contenu_html, "html.parser")

        # Extraction des données
        libelle = extraire_libelle_emploi_EMP(objet_parser_html)
        entreprise = extraire_nom_entreprise_EMP(objet_parser_html)
        ville = extraire_ville_emploi_EMP(objet_parser_html)
        texte = extraire_texte_emploi_EMP(objet_parser_html)

        # Ajout dans la liste des résultats
        donnees_extraites.append({
            "cle_unique": cle,
            "localisation": localisation,
            "nomSociete": entreprise,
            "villeEmploi": ville,
            "libelleEmploi": libelle,
            "Descriptif": texte
        })

        # Affichage console (contrôle visuel)
        print('=' * 80)
        print("INFO EMP LINKEDIN - nom de la société ==> " + entreprise)
        print("INFO EMP LINKEDIN - ville de l'emploi ==> " + ville)
        print("INFO EMP LINKEDIN - libellé de l'emploi ==> " + libelle)
        print('-' * 80)
        print("INFO EMP LINKEDIN - texte descriptif de l'emploi ==> \n" + texte[:300] + "...")
        print('=' * 80)

    except FileNotFoundError:
        print("Fichier introuvable :", chemin_complet)
        print('=' * 80)
    except Exception as e:
        print("Erreur lors du traitement :", e)
        print('=' * 80)


# ============================================================
# === SAUVEGARDE EN CSV DANS LA CURRATED ZONE
# ============================================================

output_path = "C:\\TD_DATALAKE\\projet-datalake\\TD_DATALAKE\\DATALAKE\\99_METADATA\\metadata_descriptive.csv"

df_resultats = pd.DataFrame(donnees_extraites)

# Écriture du fichier CSV avec séparateur point-virgule
df_resultats.to_csv(output_path, sep=';', index=False, encoding='utf-8-sig')

print("\nExtraction terminée avec succès !")
print(f"Fichier sauvegardé ici : {output_path}")
