import json

def get_object_by_url(data, target_url):
    for item in data:
        if item.get("url") == target_url:
            return item
    return None

# Lecture du fichier JSON depuis un fichier
with open('./data/refacto/programme-website-stats-falc-keyword-tech.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Lecture du fichier JSON depuis un fichier
with open('./data/raw/report-dashlord.json', 'r', encoding='utf-8') as fileDashlord:
    dataDashlord = json.load(fileDashlord)

# Nouvelle liste pour stocker les données mises à jour
updated_data = []

# Parcourir chaque entrée dans les données
for entry in data['data']:
    if len(entry["website_url"]) > 0:
        entry["dashlord"] = get_object_by_url(dataDashlord, entry["website_url"][0])

        # Ajouter l'entrée mise à jour à la nouvelle liste
        updated_data.append(entry)

# Nouveau dictionnaire avec les données mises à jour
updated_json = {
    "data": updated_data
}

# Conversion du dictionnaire en chaîne JSON
updated_json_str = json.dumps(updated_json, indent=4)

# Écriture des données mises à jour dans le fichier JSON
with open("data/complete/program-with-dashlord.json", 'w', encoding='utf-8') as f:
    json.dump(updated_json, f, ensure_ascii=False, indent=4)
