import json
import os
import requests
from PyPDF2 import PdfReader
from io import BytesIO


def extract_text_from_pdf(pdf_file):
    """
    Extrait le texte d'un fichier PDF.

    Args:
    pdf_file (file-like object): Le fichier PDF à partir duquel extraire le texte.

    Returns:
    str: Le contenu texte du fichier PDF.
    """
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Impossible d'extraire le texte du PDF : {e}"


def download_file(numPanneau, listName):
    """
    Télécharge un fichier depuis une URL et le sauvegarde dans le chemin de destination spécifié.

    Args:
    url (str): L'URL du fichier à télécharger.
    destination_path (str): Le chemin complet où le fichier sera sauvegardé.
    """
    try:
        destination_path = "./data/program/" + str(numPanneau) + "/" + listName + ".pdf"
        url = "https://programme-candidats.interieur.gouv.fr/elections-europeennes-2024/data-pdf-propagandes/" + listName + ".pdf"
        # Assurer que le dossier de destination existe
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        # Télécharger le fichier
        response = requests.get(url)
        response.raise_for_status()  # Vérifie si la requête a réussi

        # Sauvegarder le fichier
        with open(destination_path, 'wb') as file:
            file.write(response.content)

        print(f"Le fichier a été téléchargé et sauvegardé sous {destination_path}.")

        # Extraire le contenu texte du PDF
        pdf_content = extract_text_from_pdf(BytesIO(response.content))

        # Sauvegarder le fichier texte
        with open(destination_path + ".md", 'w', encoding='utf-8') as file:
            file.write(pdf_content)


    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite lors du téléchargement du fichier : {e}")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


# Lecture du fichier JSON depuis un fichier
with open('./data/raw/programme-falc.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Nouvelle liste pour stocker les données mises à jour
updated_data = []

# Parcourir chaque entrée dans les données
for entry in data['data']:
    # Déterminer les nouveaux champs booléens
    has_pdf = (entry['pdf'] != "0" and entry['pdf_acc'] == "0") or (entry['pdf'] == "0" and entry['pdf_acc'] != "0")
    has_falc = (entry['falc'] != "0" and entry['falc_acc'] == "0") or (
            entry['falc'] == "0" and entry['falc_acc'] != "0")
    has_falc_acc = entry['falc_acc'] != "0"
    has_pdf_acc = entry['pdf_acc'] != "0"

    # Ajouter les nouveaux champs à l'entrée
    entry['has_pdf'] = has_pdf
    entry['has_falc'] = has_falc
    entry['has_falc_acc'] = has_falc_acc
    entry['has_pdf_acc'] = has_pdf_acc

    if entry['pdf'] != "0":
        download_file(entry['numPanneau'], entry['pdf'])

    if entry['falc'] != "0":
        download_file(entry['numPanneau'], entry['falc'])

    if entry['falc_acc'] != "0":
        download_file(entry['numPanneau'], entry['falc_acc'])

    if entry['pdf_acc'] != "0":
        download_file(entry['numPanneau'], entry['pdf_acc'])

    # Ajouter l'entrée mise à jour à la nouvelle liste
    updated_data.append(entry)

    # Nouveau dictionnaire avec les données mises à jour
    updated_json = {
        "data": updated_data
    }

    # Conversion du dictionnaire en chaîne JSON
    updated_json_str = json.dumps(updated_json, indent=4)

    # Affichage du nouveau JSON
    print(updated_json_str)

    # Écriture des données mises à jour dans le fichier JSON
    with open("data/refacto/programme-falc-simple.json", 'w', encoding='utf-8') as f:
        json.dump(updated_json, f, ensure_ascii=False, indent=4)
