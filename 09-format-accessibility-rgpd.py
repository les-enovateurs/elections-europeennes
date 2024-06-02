import json

# Lecture du fichier JSON depuis un fichier
with open('./data/complete/program-with-dashlord.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Nouvelle liste pour stocker les données mises à jour
updated_data = []

# Parcourir chaque entrée dans les données
for entry in data['data']:
    dashlord = entry["dashlord"]
    if len(entry["website_url"]) > 0 and dashlord != None :
        ligthhouse = dashlord["lhr"][0]
        declaration_rgpd = dashlord["declaration-rgpd"]
        mention_legales = ""
        politiques_confidentialite = ""
        for declaration in declaration_rgpd:
            if declaration["slug"] == "ml" and declaration["slug"] != "null":
                mention_legales = 1
            if declaration["slug"] == "pc" and declaration["slug"] != "null":
                politiques_confidentialite = 1
        ecoindex = dashlord["ecoindex"]
        if ecoindex is not None and len(ecoindex) > 0:
            ecoindex = ecoindex[0]
            ecoindexItems = {
                "ecoindex_score": ecoindex["score"],
                "ecoindex_grade": ecoindex["grade"],
                "ecoindex_ges": ecoindex["ges"]
            }
        else:
            ecoindexItems = {
                "ecoindex_score": None,
                "ecoindex_grade": None,
                "ecoindex_ges": None
            }

        updated_data.append({
            "nomListe" : entry["nomListe"],
            "website_url": entry["website_url"][0],
            "numPanneau": entry["numPanneau"],
            "has_pdf": entry["has_pdf"],
            "has_falc": entry["has_falc"],
            "has_falc_acc": entry["has_falc_acc"],
            "has_pdf_acc": entry["has_pdf_acc"],
            "pdf": entry["pdf"],
            "falc_acc": entry["falc_acc"],
            "pdf_acc": entry["pdf_acc"],
            "falc": entry["falc"],
            "lighthouse_acc": ligthhouse["categories"]["accessibility"]["score"],
            "rgpd_mentions_legales" : mention_legales,
            "rgpd_politiques_confidentialite" : politiques_confidentialite,
            **ecoindexItems
        })

# Nouveau dictionnaire avec les données mises à jour
updated_json = {
    "data": updated_data
}

# Conversion du dictionnaire en chaîne JSON
updated_json_str = json.dumps(updated_json, indent=4)

# Écriture des données mises à jour dans le fichier JSON
with open("data/complete/program-accessibilite-rgpd-ecoindex.json", 'w', encoding='utf-8') as f:
    json.dump(updated_json, f, ensure_ascii=False, indent=4)
