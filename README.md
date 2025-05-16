# Research Mate: Assistant de Recherche Académique

## Description

Research Mate est une application Python qui automatise la collecte, le résumé et la génération de rapports de recherche académique à partir de sources en ligne (PubMed, ArXiv, documents locaux). Elle orchestre plusieurs agents (collecte d’articles, synthèse, édition) via la librairie **crewai**, et génère des rapports au format Markdown et PDF.

## Fonctionnalités

* **Recherche d’articles** sur PubMed et ArXiv (5 résultats maximum chacun)
* **Synthèse et résumé** des contenus collectés
* **Génération de rapports** en Markdown (`report.md`) et en PDF via Streamlit (`main_streamlit.py`)
* **Interface Web** Streamlit pour lancer facilement la génération et télécharger les rapports
* **Organisation modulaire** : configuration des agents (`agents.yaml`) et des tâches (`tasks.yaml`)

## Structure du dépôt

```
├── research_mate/
│   ├── crew.py                    # Orchestrateur principal (agents, tâches)
│   ├── tools/
│   │   ├── pubmed_tool.py         # Recherche PubMed
│   │   ├── arxiv_tool.py          # Recherche ArXiv
│   │   ├── document_search_tool.py# Recherche dans documents locaux
│   └── utils.py                   # Fonctions utilitaires (sanitisation, dossiers)
├── config/
│   ├── agents.yaml                # Configuration des agents
│   └── tasks.yaml                 # Configuration des tâches
├── main.py                        # Point d’entrée CLI (`run(topic) → report.md`)
├── main_streamlit.py              # Application Streamlit pour générer et visualiser les rapports
├── requirements.txt               # Dépendances du projet
└── outputs/
    ├── articles/                  # Articles bruts téléchargés
    └── report_<topic>.pdf         # Rapport PDF généré
```

## Prérequis

* Python >= 3.8
* Clé API Google pour Gemini 1.5 Flash (définir `GOOGLE_API_KEY` dans `.env`)
* Accès internet pour interroger PubMed et ArXiv

## Installation

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/votre-utilisateur/research-mate.git
   cd research-mate
   ```
2. Créez un environnement virtuel et installez les dépendances :

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Créez un fichier `.env` à la racine :

   ```
   GOOGLE_API_KEY=Votre_Cle_API_Google
   ```

## Configuration

* **Agents et tâches** : éditez `config/agents.yaml` et `config/tasks.yaml` pour ajuster les rôles, objectifs, backstories et séquences de tâches.
* **Nombre de résultats** : par défaut, chaque outil récupère jusqu’à 5 articles. Modifiez `retmax` (PubMed) ou `max_results` (ArXiv) dans les outils si nécessaire.

## Utilisation

### Ligne de commande

Génère un rapport Markdown sur un sujet donné et le sauvegarde dans `report.md` :

```bash
python main.py "Machine Learning in Healthcare"
```

### Interface Web Streamlit

1. Lancez l’application :

   ```bash
   streamlit run main_streamlit.py
   ```
2. Saisissez votre **topic** et cliquez sur **Generate Research Report**.
3. Téléchargez les articles collectés et le PDF depuis la barre latérale.

## Exemple de rapport

* **report.md** : résumé complet produit par l’agent `edit_report`.
* **PDF** : formaté avec ReportLab, intègre titre, date, sections, listes et références.

## Contribuer

1. Forkez ce dépôt.
2. Créez une branche feature : `git checkout -b feature/ma-fonctionnalité`.
3. Commitez vos changements : `git commit -m "Ajout de ..."`
4. Poussez et ouvrez une Pull Request.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
