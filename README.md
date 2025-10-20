# Web Scraper - Outil de Scraping Web Intelligent

Un scraper web robuste et modulaire développé en Python pour extraire des données structurées depuis des sites web, avec téléchargement d'images et exploration récursive.

## 🚀 Fonctionnalités

- **Scraping récursif** jusqu'à 2 niveaux de profondeur
- **Téléchargement automatique des images** avec gestion des doublons
- **Export des données** au format JSON
- **Logging complet** pour le débogage
- **Gestion des erreurs** robuste
- **Respect de la politesse** (delay entre les requêtes)

## 📋 Prérequis

- Python 3.7 ou supérieur
- Pip (gestionnaire de packages Python)

## 🛠 Installation

1. **Cloner le repository**
```bash
git clone https://github.com/Thierry2282/scrapping.git
cd scrapping
```

2. **Créer un environnement virtuel**
```bash

python -m venv venv
```

3. **Activer l'environnement virtuel**

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```
4. **Installer les dépendances**

```bash

pip install -r requirements.txt
```