import json
from collections import Counter

def find_keyword(numPanneau, pathName, keywords):

    if numPanneau == 13:
        print("ff")

    path = "./data/program/"+str(numPanneau)+"/"+pathName+".pdf.md"

    # Convertir la liste de mots-clés en un ensemble pour une recherche rapide
    keywords_set = set(keywords)
    # Initialiser un compteur pour le nombre total d'occurrences de mots-clés
    total_count = 0

    # Ouvrir le fichier et lire ligne par ligne
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            # Compter les occurrences de chaque mot dans la ligne
            words = line.split()
            line_counts = Counter(word for word in words if word in keywords_set)
            # Ajouter le nombre total d'occurrences dans la ligne au compte total
            total_count += sum(line_counts.values())

    return total_count

# Lecture du fichier JSON depuis un fichier
with open('./data/refacto/programme-website-stats-falc.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Nouvelle liste pour stocker les données mises à jour
updated_data = []
keywordTech = ["réseaux sociaux", "cyber", "cyberdéfense", "l'IA", "(IA)", "cyberattaques", "cybersécurité", "intelligence", "artificielle", "DSA",
               "RGPD", "numerique", "numériques", "datacenter", "open source","TikTok"
               "données personnelles"]

# Parcourir chaque entrée dans les données
for entry in data['data']:

    entry['hasTech'] = 0

    if entry['pdf_acc'] != "0":
        occurenceTechKeyword = find_keyword(entry['numPanneau'], entry['pdf_acc'], keywordTech)
        if occurenceTechKeyword:
            entry['hasTech'] = {
                "name": 'pdf_acc',
                "occurence": occurenceTechKeyword
            }

    if entry['hasTech'] == 0 and entry['falc_acc'] != "0":
        occurenceTechKeyword = find_keyword(entry['numPanneau'], entry['falc_acc'], keywordTech)
        if occurenceTechKeyword:
            entry['hasTech'] = {
                "name": 'falc_acc',
                "occurence": occurenceTechKeyword
            }

    if entry['hasTech'] == 0 and entry['pdf'] != "0":
        occurenceTechKeyword = find_keyword(entry['numPanneau'], entry['pdf'], keywordTech)
        if occurenceTechKeyword:
            entry['hasTech'] = {
                "name": 'pdf',
                "occurence": occurenceTechKeyword
            }

    if entry['hasTech'] == 0 and entry['falc'] != "0":
        occurenceTechKeyword = find_keyword(entry['numPanneau'], entry['falc'], keywordTech)
        if occurenceTechKeyword:
            entry['hasTech'] = {
                "name": 'falc',
                "occurence": occurenceTechKeyword
            }

    # Ajouter l'entrée mise à jour à la nouvelle liste
    updated_data.append(entry)

# Nouveau dictionnaire avec les données mises à jour
updated_json = {
    "data": updated_data
}

# Conversion du dictionnaire en chaîne JSON
updated_json_str = json.dumps(updated_json, indent=4)

# Écriture des données mises à jour dans le fichier JSON
with open("data/refacto/programme-website-stats-falc-keyword-tech.json", 'w', encoding='utf-8') as f:
    json.dump(updated_json, f, ensure_ascii=False, indent=4)
