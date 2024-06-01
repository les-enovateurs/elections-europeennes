import json

# Lecture du fichier JSON depuis un fichier
with open('./data/refacto/programme-website-custom-url.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Nouvelle liste pour stocker les données mises à jour
updated_data = []

# Parcourir chaque entrée dans les données
for entry in data['data']:

    with open('./data/stats/'+str(entry["numPanneau"])+"/repartition_parite.json", 'r', encoding='utf-8') as file:
        parite = json.load(file)
        entry["parite"] = parite

    with open('./data/stats/'+str(entry["numPanneau"])+"/repartition_professions_partie.json", 'r', encoding='utf-8') as file:
        repartition_professions_partie = json.load(file)
        entry["professions"] = repartition_professions_partie

    with open('./data/stats/'+str(entry["numPanneau"])+"/repartition_tranches_age.json", 'r', encoding='utf-8') as file:
        repartition_age = json.load(file)
        entry["age"] = repartition_age

    # Ajouter l'entrée mise à jour à la nouvelle liste
    updated_data.append(entry)

# Nouveau dictionnaire avec les données mises à jour
updated_json = {
    "data": updated_data
}

# Conversion du dictionnaire en chaîne JSON
updated_json_str = json.dumps(updated_json, indent=4)

# Écriture des données mises à jour dans le fichier JSON
with open("data/refacto/programme-website-stats-falc.json", 'w', encoding='utf-8') as f:
    json.dump(updated_json, f, ensure_ascii=False, indent=4)
