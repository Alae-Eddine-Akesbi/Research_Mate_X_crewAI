# Research Mate 🚀

**Assistant de Recherche Académique** permettant d’automatiser la collecte, la synthèse et la génération de rapports à partir de sources scientifiques.

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-%3E%3D1.0-green)](https://streamlit.io/)
[![Licence MIT](https://img.shields.io/badge/licence-MIT-yellow.svg)](LICENSE)

---

## 🌟 Description

Research Mate offre un pipeline complet pour :

1. **Collecter** des articles via PubMed, ArXiv et vos documents locaux.
2. **Synthétiser** et résumer les contenus avec **Gemini 1.5 Flash** (API Google Cloud).
3. **Générer** des rapports en **Markdown** et **PDF** depuis une CLI ou une interface **Streamlit**.

L’architecture repose sur **crewai**, orchestration d’agents intelligents pour chaque étape.

---

## 🔧 Fonctionnalités

* 🔍 **Recherche PubMed** (jusqu’à 5 résultats) via `tools/pubmed_tool.py`
* 📄 **Recherche ArXiv** (jusqu’à 5 résultats) via `tools/arxiv_tool.py`
* 📂 **Indexation locale** des PDF et Markdown via `tools/document_search_tool.py`
* 🤖 **Synthèse intelligente** avec **Gemini 1.5 Flash** (modèle `gemini/gemini-1.5-flash`)
* 📑 **Rapport Markdown** (`outputs/report_<topic>.md`)
* 📚 **PDF** stylisé via **Streamlit** + **ReportLab** (`outputs/report_<topic>.pdf`)
* 🌐 **Interface Web** Streamlit pour générer, visualiser et télécharger
* ⚙️ **Configuration** modulaire via `config/agents.yaml` et `config/tasks.yaml`

---

## 📂 Structure du projet

```plaintext
├── research_mate/
│   ├── crew.py                   # Orchestrateur principal
│   ├── tools/                    # Implémentation des outils de collecte
│   │   ├── pubmed_tool.py
│   │   ├── arxiv_tool.py
│   │   └── document_search_tool.py
│   └── utils.py                  # Helpers (sanitisation, création de dossiers)
├── config/
│   ├── agents.yaml               # Définition des agents (roles, objectifs)
│   └── tasks.yaml                # Workflow (séquence et config des tâches)
├── main.py                       # CLI : génère `report.md`
├── main_streamlit.py             # Interface Web + génération PDF
├── pyproject.toml                # Configuration du package
├── requirements.txt              # Dépendances Python
├── .env                          # Variables d’environnement (non versionné)
└── outputs/                      # Dossiers et rapports générés
    ├── articles/                 # Articles bruts (.txt)
    ├── report_<topic>.md         # Rapport Markdown
    └── report_<topic>.pdf        # Rapport PDF
```

---

## ⚙️ Prérequis & Installation

1. **Clonez** le dépôt :

   ```bash
   ```

git clone [https://github.com/votre-utilisateur/research-mate.git](https://github.com/votre-utilisateur/research-mate.git)
cd research-mate

````
2. **Créez** un environnement virtuel et installez les dépendances :
    ```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
````

3. **Configurez** vos clés API :

   ```bash
   ```

# Fichier .env

MODEL=gemini/gemini-1.5-flash
GOOGLE\_API\_KEY=Votre\_Cle\_Google\_Cloud

````
4. **Vérifiez** l’accès Internet pour PubMed et ArXiv.

---

## 🚀 Utilisation

### 1. Ligne de commande (CLI)

```bash
# Générer un rapport Markdown
python main.py "Machine Learning in Healthcare"
# Résultat -> outputs/report_Machine_Learning_in_Healthcare.md
````

### 2. Interface Web (Streamlit)

```bash
streamlit run main_streamlit.py
```

1. Saisissez votre **topic** 🔎
2. Cliquez sur **Generate Research Report** 📚
3. Téléchargez articles, Markdown et PDF depuis la barre latérale 📰

---

## 🛠️ Personnalisation avancée

* **Nombre de résultats** : modifiez `retmax` (PubMed) et `max_results` (ArXiv) dans les outils.
* **Agents & tâches** : adaptez `config/agents.yaml` et `config/tasks.yaml` pour changer rôles, objectifs, séquences.
* **Prompts & résumés** : ajustez les fonctions de `research_mate.utils` pour modifier la longueur ou le style des résumés.

---

## 🧱 Packaging & Scripts

* **pyproject.toml** définit le package `research_mate` (version 0.1.0).
* Entrypoints CLI disponibles :

  * `research_mate` -> `research_mate.main:run`
  * `run_crew`      -> `research_mate.main:run`

---


## 📄 Licence

Ce projet est sous licence **MIT**. Voir [LICENSE](LICENSE) pour plus de détails.
