import pandas as pd
import matplotlib.pyplot as plt
import os
import json
import re

# Lire les données à partir du fichier CSV
df = pd.read_csv("./data/raw/candidats-eur-2024.csv", delimiter=";")

pattern = re.compile(r'\(\d+\) - ')

# Parcourir les parties et générer les camemberts
for partie, partie_data in df.groupby('Numéro de panneau'):
    # Créer un dossier pour la partie
    dossier_partie = f"./data/stats/{partie}"
    os.makedirs(dossier_partie, exist_ok=True)

    partie_data['Profession'] = partie_data['Profession'].str.replace(pattern, '')

    # Générer le camembert pour les professions de cette partie
    profession_counts = partie_data['Profession'].value_counts()

    plt.figure(figsize=(12, 8))
    profession_counts.plot(kind='pie', autopct=lambda p: f'{p:.1f}%', startangle=140)
    plt.title(f'Répartition des professions')
    plt.axis('equal')  # Assurez-vous que le camembert est un cercle

    # Enregistrer le graphique dans le dossier de la partie
    # plt.savefig(os.path.join(dossier_partie, f'camembert_professions_partie.png'))
    plt.savefig(os.path.join(dossier_partie, f'camembert_professions_partie.svg'), format='svg', dpi=300)
    plt.close()

    # Calculate percentages
    profession_percentages = profession_counts / profession_counts.sum() * 100

    # Prepare the age distribution with percentages for JSON
    profession_distribution_dict = profession_percentages.round(1).to_dict()

    with open(os.path.join(dossier_partie, f'repartition_professions_partie.json'), 'w') as json_file:
        json.dump(profession_distribution_dict, json_file, indent=4, ensure_ascii=False)

    parite_counts = partie_data['Sexe'].value_counts()

    plt.figure(figsize=(12, 8))
    parite_counts.plot(kind='pie', autopct=lambda p: f'{p:.1f}%', startangle=140)
    plt.title(f'Parité')
    plt.axis('equal')  # Assurez-vous que le camembert est un cercle

    # Enregistrer le graphique dans le dossier de la partie
    # plt.savefig(os.path.join(dossier_partie, f'camembert_professions_partie.png'))
    plt.savefig(os.path.join(dossier_partie, f'camembert_parite.svg'), format='svg', dpi=300)
    plt.close()

    # Calculate percentages
    parite_percentages = parite_counts / parite_counts.sum() * 100

    # Prepare the age distribution with percentages for JSON
    parite_distribution_dict = parite_percentages.round(1).to_dict()

    with open(os.path.join(dossier_partie, f'repartition_parite.json'), 'w') as json_file:
        json.dump(parite_distribution_dict, json_file, indent=4, ensure_ascii=False)

    # Convertir la colonne 'Date de naissance' en datetime
    partie_data['Date de naissance'] = pd.to_datetime(partie_data['Date de naissance'], format='%d/%m/%Y')

    # Calculer l'âge à partir de la date de naissance
    partie_data['Age'] = pd.Timestamp.now().year - partie_data['Date de naissance'].dt.year

    # Définir les tranches d'âges
    bins = [18, 30, 40, 50, 60, 70, 120]
    labels = ['18-29', '30-39', '40-49', '50-59', '60-69', '70+']

    # Ajouter une colonne pour les tranches d'âges
    partie_data['Tranche d\'âge'] = pd.cut(partie_data['Age'], bins=bins, labels=labels, right=False)

    # Générer le camembert pour les tranches d'âge de cette partie
    age_counts = partie_data['Tranche d\'âge'].value_counts()

    plt.figure(figsize=(8, 6))
    age_counts.plot(kind='pie', autopct=lambda p: f'{p:.1f}%', startangle=140)
    plt.title(f'Répartition des tranches d\'âge')
    plt.axis('equal')  # Assurez-vous que le camembert est un cercle

    # Enregistrer le graphique dans le dossier de la partie
    # plt.savefig(os.path.join(dossier_partie, f'camembert_tranches_age_partie.png'))
    plt.savefig(os.path.join(dossier_partie, f'camembert_tranches_age_partie.svg'), format='svg', dpi=300)
    plt.close()

    # Calculate percentages
    age_percentages = age_counts / age_counts.sum() * 100

    # Prepare the age distribution with percentages for JSON
    age_distribution_dict = age_percentages.round(1).to_dict()
    # Round to match the pie chart display
    with open(os.path.join(dossier_partie, f'repartition_tranches_age.json'), 'w') as json_file:
        json.dump(age_distribution_dict, json_file, indent=4, ensure_ascii=False)