import csv
import os
import re
import unicodedata

# == FONCTION DE NORMALISATION ==
def normalize_key(text):
    """
    Normalise un texte :
    - Met en minuscules
    - Supprime les accents (diacritiques)
    - Remplace la ponctuation par un espace
    - Réduit les espaces multiples
    """
    if not text:
        return ""
    
    # 1. Minuscules
    s = str(text).lower()
    
    # 2. Suppression des accents
    s = unicodedata.normalize('NFD', s)
    s = s.encode('ascii', 'ignore').decode('utf-8')
    
    # 3. Remplace ponctuation par un espace
    s = re.sub(r'[^a-z0-9\s]', ' ', s) 
    
    # 4. Réduire les espaces multiples
    s = re.sub(r'\s+', ' ', s).strip()
    return s

# == CHEMINS DES FICHIERS ==

# Le fichier que vous avez trouvé (avec "nom_commune_complet", etc.)
FICHIER_REFERENCE_VILLES = 'communes-france.csv' 
# Le fichier de sortie de votre premier script
FICHIER_ENTREE_SOCIETES = 'societes.csv'
# Le fichier final qui contiendra les données complétées
FICHIER_SORTIE_ENRICHI = 'societes_enrichies.csv'


def charger_reference_villes(chemin_fichier):
    """
    Charge le fichier CSV des villes dans un dictionnaire
    pour une recherche rapide.
    
    --- MODIFIÉ pour gérer "Lyon 01" ET "Lyon" ---
    """
    lookup_db = {}
    print(f"Chargement du fichier de référence : {chemin_fichier}...")
    try:
        # Utilisation de 'latin-1' qui a corrigé votre erreur d'encodage
        with open(chemin_fichier, mode='r', encoding='latin-1') as f: 
            
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(f.read(1024))
            f.seek(0)
            lecteur = csv.DictReader(f, dialect=dialect) 
            
            noms_colonnes_test = ['nom_commune_complet', 'code_postal', 'nom_region']
            if not all(col in lecteur.fieldnames for col in noms_colonnes_test):
                print(f"ERREUR: Colonnes manquantes. Fichier '{chemin_fichier}'")
                print(f"  Doit contenir : {noms_colonnes_test}")
                print(f"  Colonnes trouvées : {lecteur.fieldnames}")
                return None

            for ligne in lecteur:
                ville_brute = ligne.get('nom_commune_complet') # ex: "Lyon 01"
                code_postal = ligne.get('code_postal')
                region_brute = ligne.get('nom_region')

                if not ville_brute:
                    continue
                    
                # 1. Normaliser la clé exacte (ex: "Lyon 01" -> "lyon 01")
                cle_exacte = normalize_key(ville_brute)
                region_normalisee = normalize_key(region_brute)

                info = {
                    'postal': code_postal or '',
                    'region': region_normalisee
                }

                # ===============================================
                #  LOGIQUE DE CLÉ DE BASE
                # ===============================================
                # On crée une clé "de base" en supprimant les chiffres
                # d'arrondissement (ex: "lyon 01" -> "lyon")
                # et les mentions "cedex" (ex: "ecully cedex" -> "ecully")
                cle_base = re.sub(r'(\s+\d{1,2}|\s+cedex.*)$', '', cle_exacte).strip()
                # ===============================================

                # 2. Enregistrer la clé exacte (ex: "lyon 01")
                if cle_exacte not in lookup_db:
                    lookup_db[cle_exacte] = info
                
                # 3. Enregistrer la clé de base (ex: "lyon")
                #    UNIQUEMENT si elle est différente ET n'existe pas encore
                #    (Cela garantit que "lyon" pointera vers "lyon 01")
                if cle_base and cle_base != cle_exacte and cle_base not in lookup_db:
                    lookup_db[cle_base] = info
                    
    except FileNotFoundError:
        print(f"ERREUR: Fichier de référence '{chemin_fichier}' introuvable.")
        print("Veuillez le télécharger et le placer dans le même dossier.")
        return None
    except Exception as e:
        print(f"ERREUR lors de la lecture du fichier de référence : {e}")
        print("Vérifiez le format du fichier (encodage, délimiteur).")
        return None
        
    print(f"Base de données de référence chargée : {len(lookup_db)} villes.")
    return lookup_db

def enrichir_societes(lookup_db):
    """
    Lit le fichier societes.csv et le ré-écrit en version enrichie.
    (Version simplifiée)
    """
    lignes_enrichies = []
    lignes_modifiees = 0
    
    try:
        # Votre fichier societes.csv est en UTF-8 (créé par votre 1er script)
        with open(FICHIER_ENTREE_SOCIETES, mode='r', encoding='utf-8') as f_in:
            lecteur = csv.DictReader(f_in, delimiter=';')
            headers = lecteur.fieldnames
            
            if not headers:
                print(f"ERREUR: Le fichier '{FICHIER_ENTREE_SOCIETES}' est vide ou mal formaté.")
                return

            for row in lecteur:
                ville = row.get('villeSociete', '') # ex: "lyon", "lyon 03", "ecully"
                postal = row.get('codePostalSociete', '')
                region = row.get('regionSociete', '')
                
                modifie = False
                info = None

                if ville:
                    # 1. Essayer une correspondance (ex: "lyon 03" ou "lyon")
                    #    'ville' est déjà normalisée par votre premier script.
                    info = lookup_db.get(ville)
                
                # 2. Si on a trouvé des infos
                if info:
                    # On ne remplit que ce qui est vide
                    if not postal and info.get('postal'):
                        row['codePostalSociete'] = info['postal']
                        modifie = True
                    if not region and info.get('region'):
                        row['regionSociete'] = info['region']
                        modifie = True
                
                if modifie:
                    lignes_modifiees += 1
                lignes_enrichies.append(row)

    except FileNotFoundError:
        print(f"ERREUR: Fichier d'entrée '{FICHIER_ENTREE_SOCIETES}' introuvable.")
        print("Assurez-vous d'avoir d'abord lancé votre premier script.")
        return
    except Exception as e:
        print(f"ERREUR inattendue en lisant {FICHIER_ENTREE_SOCIETES}: {e}")
        return

    # Écriture du nouveau fichier enrichi
    try:
        with open(FICHIER_SORTIE_ENRICHI, 'w', newline='', encoding='utf-8') as f_out:
            writer = csv.DictWriter(f_out, fieldnames=headers, delimiter=';')
            writer.writeheader()
            writer.writerows(lignes_enrichies)
        print(f"✅ Fichier '{os.path.abspath(FICHIER_SORTIE_ENRICHI)}' créé avec succès.")
        print(f"   {lignes_modifiees} lignes ont été enrichies.")
    except Exception as e:
        print(f"ERREUR lors de l'écriture du fichier de sortie : {e}")


# --- Point d'entrée principal du script ---
if __name__ == "__main__":
    print("--- Démarrage de l'enrichissement des sociétés ---")
    
    # 1. Charger la base de données des villes
    db_villes = charger_reference_villes(FICHIER_REFERENCE_VILLES)
    
    # 2. Si le chargement a réussi, enrichir le fichier
    if db_villes:
        print(f"\n--- Enrichissement de {FICHIER_ENTREE_SOCIETES} ---")
        enrichir_societes(db_villes)