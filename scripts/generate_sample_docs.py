import os
from pathlib import Path
from rich.console import Console

console = Console()

DOCS = {
    "probiotiques.txt": (
        "L'efficacité des probiotiques sur l'immunité\n\n"
        "Des études récentes montrent que la consommation régulière de probiotiques, "
        "notamment Lactobacillus et Bifidobacterium, améliore la réponse immunitaire intestinale. "
        "Il y a un fort consensus sur le fait que ces bactéries bénéfiques réduisent l'incidence "
        "et la durée des infections des voies respiratoires supérieures chez les adultes en bonne santé. "
        "Cependant, l'impact sur les personnes immunodéprimées reste incertain et nécessite "
        "davantage d'essais cliniques."
    ),
    "anti_inflammatoires.txt": (
        "Les anti-inflammatoires et les maladies chroniques\n\n"
        "L'inflammation chronique est un facteur clé dans le développement de maladies cardiovasculaires "
        "et métaboliques. L'utilisation prolongée d'AINS (anti-inflammatoires non stéroïdiens) "
        "présente des risques gastriques et cardiovasculaires majeurs. De nouveaux traitements "
        "ciblant spécifiquement des cytokines telles que l'IL-6 montrent des résultats prometteurs "
        "pour réduire l'inflammation systémique avec moins d'effets secondaires, créant un espoir "
        "pour la médecine préventive."
    ),
    "sommeil_immunite.txt": (
        "L'impact du sommeil sur l'immunité\n\n"
        "Le manque de sommeil réduit drastiquement la production de cytokines, des protéines "
        "essentielles à la lutte contre les infections. Les individus dormant moins de six heures "
        "par nuit ont un taux d'infection virale supérieur de 4,2 fois par rapport à ceux "
        "dormant huit heures ou plus. Un consensus scientifique établit que la privation de sommeil "
        "affecte l'efficacité des vaccins, notamment celui de la grippe. L'hygiène du sommeil "
        "est désormais considérée comme une recommandation médicale majeure."
    ),
    "car_t_therapies.txt": (
        "Innovations des thérapies CAR-T en oncologie\n\n"
        "Les thérapies par cellules T à récepteur chimérique (CAR-T) ont révolutionné le "
        "traitement de certaines leucémies et lymphomes. En modifiant génétiquement les "
        "lymphocytes du patient pour qu'ils attaquent les cellules cancéreuses, des taux "
        "de rémission extrêmement élevés ont été observés. Néanmoins, les coûts exorbitants "
        "et la toxicité neurologique (syndrome de relargage des cytokines) limitent "
        "actuellement l'application de ces traitements aux cancers solides."
    ),
    "ia_medecine.txt": (
        "La médecine préventive et l'Intelligence Artificielle\n\n"
        "L'intelligence artificielle transforme la médecine préventive en permettant une "
        "analyse prédictive à partir des dossiers médicaux électroniques. Les algorithmes de "
        "Deep Learning surpassent désormais les spécialistes dans la détection précoce des "
        "Mélanomes ou des rétinopathies diabétiques. Bien que ces avancées soient prometteuses, "
        "les divergences s'accentuent quant à l'explicabilité de ces modèles (boîte noire) et "
        "au risque de biais algorithmiques défavorisant certaines minorités ethniques."
    )
}

def main():
    # We create the folder based on the current directory so it works from anywhere inside medisearch/
    data_dir = Path("data/raw")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    console.print(f"[bold blue]Création des documents factices dans [cyan]{data_dir.absolute()}[/cyan][/bold blue]")
    
    for filename, content in DOCS.items():
        file_path = data_dir / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        console.print(f"  [green]✓[/green] {filename} créé.")
    
    console.print("[bold green]Génération terminée avec succès ![/]")

if __name__ == "__main__":
    main()

