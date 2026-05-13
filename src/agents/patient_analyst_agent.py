import json
import os


class PatientAnalystAgent:
    """Agent spécialisé dans le diagnostic différentiel basé sur le profil patient."""

    def __init__(self, llm):
        self.llm = llm

    def format_patient_profile(self, patient: dict) -> str:
        """Formate les données patient en texte clinique structuré."""
        lines = [
            f"=== DOSSIER PATIENT ===",
            f"Nom : {patient['nom']}",
            f"Âge : {patient['age']} ans | Sexe : {patient['sexe']}",
            f"Durée des symptômes : {patient.get('duree_symptomes', 'Non précisée')}",
            f"\nSYMPTÔMES PRINCIPAUX :",
            "  - " + "\n  - ".join(patient.get("symptomes", [])),
            f"\nANTÉCÉDENTS MÉDICAUX :",
            "  - " + "\n  - ".join(patient.get("antecedents", ["Aucun"])) if patient.get("antecedents") else "  - Aucun",
            f"\nTRAITEMENTS EN COURS :",
            "  - " + "\n  - ".join(patient.get("traitements_actuels", ["Aucun"])) if patient.get("traitements_actuels") else "  - Aucun",
            f"\nMESURES CLINIQUES :",
        ]
        for k, v in patient.get("mesures", {}).items():
            lines.append(f"  - {k} : {v}")
        return "\n".join(lines)

    def analyze(self, patient: dict, rag_context: str = "") -> str:
        """Génère un diagnostic différentiel et une décision médicale."""
        profile = self.format_patient_profile(patient)

        rag_section = f"\nCONTEXTE MÉDICAL (base de connaissances) :\n{rag_context}" if rag_context else ""

        prompt = f"""Tu es un médecin expert en diagnostic différentiel. Analyse ce dossier patient avec rigueur.

{profile}
{rag_section}

Génère une analyse médicale structurée en Markdown avec :

## Diagnostics différentiels
Liste les 3 diagnostics les plus probables avec pourcentage de probabilité et justification clinique.

## Niveau d'urgence
Indique : CRITIQUE / URGENT / SEMI-URGENT / NON-URGENT avec justification.

## Examens complémentaires recommandés
Liste les examens biologiques et d'imagerie à prescrire en priorité.

## Plan de prise en charge
Orientation (urgences, médecin généraliste, spécialiste) + traitement initial proposé.

## Alertes cliniques
Signaux d'alarme à surveiller impérativement.

Réponds uniquement en Markdown structuré, en français, de façon professionnelle et concise.
"""
        response = self.llm.invoke(prompt)
        return str(response.content)
