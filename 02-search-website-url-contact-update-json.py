import json
import re

def find_urls_and_emails(file_path):
    """
    Lit un fichier et cherche des URLs et des adresses e-mail.

    Args:
    file_path (str): Le chemin du fichier à lire.

    Returns:
    tuple: Un tuple contenant une liste d'URLs et une liste d'adresses e-mail trouvées.
    """
    urls = []
    emails = []

    # Ouvre le fichier en mode lecture
    with open(file_path, 'r', encoding='utf-8') as file:
        # Lit le contenu du fichier ligne par ligne
        for line in file:
            # Recherche des URLs dans la ligne
            urls.extend(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line))

            # Recherche des adresses e-mail dans la ligne
            emails.extend(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', line))

    return list(set(urls)), list(set(emails))

# Lecture du fichier JSON depuis un fichier
with open('./data/refacto/programme-falc-simple.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Nouvelle liste pour stocker les données mises à jour
updated_data = []

# Parcourir chaque entrée dans les données
for entry in data['data']:

    website_url = []
    contact_mail = []

    if entry['pdf_acc'] != "0":
        website_url, contact_mail = find_urls_and_emails("./data/program/"+str(entry['numPanneau'])+"/"+entry['pdf_acc']+".pdf.md")

    if website_url == [] and entry['falc_acc'] != "0":
        website_url, contact_mail = find_urls_and_emails("./data/program/"+str(entry['numPanneau'])+"/"+entry['falc_acc']+".pdf.md")

    if website_url == [] and entry['pdf'] != "0":
        website_url, contact_mail = find_urls_and_emails("./data/program/"+str(entry['numPanneau'])+"/"+entry['pdf']+".pdf.md")

    if website_url == [] and entry['falc'] != "0":
        website_url, contact_mail = find_urls_and_emails("./data/program/"+str(entry['numPanneau'])+"/"+entry['falc']+".pdf.md")

    entry["contact_mail"] = contact_mail
    entry["website_url"] = website_url

    # Ajouter l'entrée mise à jour à la nouvelle liste
    updated_data.append(entry)

# Nouveau dictionnaire avec les données mises à jour
updated_json = {
    "data": updated_data
}

# Conversion du dictionnaire en chaîne JSON
updated_json_str = json.dumps(updated_json, indent=4)

# Écriture des données mises à jour dans le fichier JSON
with open("data/refacto/programme-contact-url.json", 'w', encoding='utf-8') as f:
    json.dump(updated_json, f, ensure_ascii=False, indent=4)


