import pandas as pd
from bs4 import BeautifulSoup
import os

# ============================================================
# === PHASE 2 - EXTRACTION : Lecture du CSV et affichage des fichiers HTML
# ============================================================

metadata_path = "C:\\TD_DATALAKE\\projet-datalake\\TD_DATALAKE\\DATALAKE\\99_METADATA\\metadata_technique.csv"

metadata = pd.read_csv(metadata_path, sep=';', quotechar='"')

print("Fichier de métadonnées chargé avec succès.\n")

grouped = metadata.groupby("cle_unique")


#==============================================================================
#-- LINKEDIN (EMPLOI) : Libellé de l'offre
#==============================================================================
def extraire_libelle_emploi_EMP(objet_html):
    texte_tmp = objet_html.find_all('h1', attrs={'class': 'topcard__title'})
    if not texte_tmp:
        return 'NULL'
    return texte_tmp[0].get_text(strip=True) or 'NULL'


#==============================================================================
#-- LINKEDIN (EMPLOI) : Nom de la Société demandeuse
#==============================================================================
def extraire_nom_entreprise_EMP(objet_html):
    texte_tmp = objet_html.find_all('span', attrs={'class': 'topcard__flavor'})
    if not texte_tmp:
        return 'NULL'
    return texte_tmp[0].get_text(strip=True) or 'NULL'


#==============================================================================
#-- LINKEDIN (EMPLOI) : Ville de l'emploi proposé
#==============================================================================
def extraire_ville_emploi_EMP(objet_html):
    texte_tmp = objet_html.find_all('span', attrs={'class': 'topcard__flavor topcard__flavor--bullet'})
    if not texte_tmp:
        return 'NULL'
    return texte_tmp[0].get_text(strip=True) or 'NULL'


#==============================================================================
#-- LINKEDIN (EMPLOI) : Texte de l'offre d'emploi
#==============================================================================
def extraire_texte_emploi_EMP(objet_html):
    texte_tmp = objet_html.find_all('div', attrs={"class": "description__text description__text--rich"})
    if not texte_tmp:
        return 'NULL'
    return texte_tmp[0].get_text(strip=True) or 'NULL'


# ============================================================
# === PARCOURS DES FICHIERS HTML ET EXTRACTION DES DONNÉES
# ============================================================

# Liste pour stocker les résultats au format clé/colonne/valeur
donnees_extraites = []

for cle, group in grouped:
    dico = dict(zip(group["colonne"], group["valeur"]))
    localisation = dico.get("localisation_du_fichier_html", "NON TROUVÉE")
    nom_fichier = dico.get("nom_du_fichier_html", "NON TROUVÉ")

    if "LINKEDIN/EMP" not in localisation.upper():
        continue

    chemin_complet = os.path.join("C:\\TD_DATALAKE\\projet-datalake", localisation.replace("/", "\\"))

    print(f"\nClé unique : {cle}")
    print(f"Nom du fichier : {nom_fichier}")
    print(f"Localisation complète : {chemin_complet}")
    print("-" * 80)

    try:
        with open(chemin_complet, "r", encoding="utf-8") as f:
            contenu_html = f.read()

        objet_parser_html = BeautifulSoup(contenu_html, "html.parser")

        libelle = extraire_libelle_emploi_EMP(objet_parser_html)
        entreprise = extraire_nom_entreprise_EMP(objet_parser_html)
        ville = extraire_ville_emploi_EMP(objet_parser_html)
        texte = extraire_texte_emploi_EMP(objet_parser_html)

        # Ajout des données au format "clé / colonne / valeur"
        donnees_extraites.append({"cle_unique": cle, "colonne": "nomSociete", "valeur": entreprise})
        donnees_extraites.append({"cle_unique": cle, "colonne": "villeEmploi", "valeur": ville})
        donnees_extraites.append({"cle_unique": cle, "colonne": "libelleEmploi", "valeur": libelle})
        donnees_extraites.append({"cle_unique": cle, "colonne": "Descriptif", "valeur": texte})
        #donnees_extraites.append({"cle_unique": cle, "colonne": "localisation", "valeur": localisation})

        print('=' * 80)
        print(f"INFO EMP LINKEDIN - nom de la société ==> {entreprise}")
        # print(f"INFO EMP LINKEDIN - ville de l'emploi ==> {ville}")
        # print(f"INFO EMP LINKEDIN - libellé de l'emploi ==> {libelle}")
        # print('-' * 80)
        # print(f"INFO EMP LINKEDIN - texte descriptif ==> \n{texte[:300]}...")
        # print('=' * 80)

    except FileNotFoundError:
        print("Fichier introuvable :", chemin_complet)
        print('=' * 80)
    except Exception as e:
        print("Erreur lors du traitement :", e)
        print('=' * 80)


# ============================================================
# === SAUVEGARDE EN CSV FORMAT LONG (clé / colonne / valeur)
# ============================================================

output_path = "C:\\TD_DATALAKE\\projet-datalake\\TD_DATALAKE\\DATALAKE\\99_METADATA\\metadata_descriptive.csv"

df_resultats = pd.DataFrame(donnees_extraites)

df_resultats.to_csv(output_path, sep=';', index=False, encoding='utf-8-sig')

print("\nExtraction terminée avec succès !")
print(f"Fichier sauvegardé ici : {output_path}")
