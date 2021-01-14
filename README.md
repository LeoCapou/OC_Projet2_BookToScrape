# OC_Projet2_BookToScrape

Second projet de la formation "Développeur d'application - Python" d'OpenClassrooms dont le but est de récupérer les informations suivantes pour chaque livre présent sur le site [Books ToScrape](https://books.toscrape.com/):
- product_page_url
- universal_ product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url

Ces informations sont enregistrées dans un fichier CSV pour chaque catégorie de livres et les images de couvertures de tous les livres sont également enregistrées dans le dossier "Images".

## Pour commencer

Ces instructions vous permettent de récupérer une copie du projet pour le tester sur votre machine.

### Prerequis

Ce programme étant basé sur Python, il est nécessaire que celui-ci soit installé sur votre machine.
Vous pouvez télécharger Python [ici](https://www.python.org/downloads/)

### Installation

Pour ne pas entrer en conflit avec d'autres projets déjà existants, il est préférable d'exécuter le programme sous un environnement virtuel.

Voici les principales commandes pour:

1. créer l'environnement virtuel

```
python3 -m venv tutorial-env
```
2. activer l'environnement virtuel

```
tutorial-env\Scripts\activate.bat
```

Pour plus de détails sur l'installation d'un environnement virtuel, se reporter à [la documentation Python](https://docs.python.org/fr/3.6/tutorial/venv.html)

Il est également nécessaire d'installer les bibliothèques indispensables au bon fonctionnement du programme. 
Celles-ci sont listées dans le document `requirement.txt` et leur installation se fait via la commande suivante exécutée dans l'environnement virtuel que vous venez de créer:
```
pip install -r requirements.txt
```

## Exécution du programme

Une fois la console placée dans le dossier du programme, il suffit d'exécuter la commande suivante dans l'environnement virtuel:
```
python3 main.py
```
Des dossiers `CSV` et `Images` vont se créer. Ils contiendront respectivement les fichiers CSV de chaque catégorie de livre ainsi que toutes les images de couverture.
Vous pourrez suivre l'évolution du programme grâce à l'affichage de la catégorie en cours d'extraction sur la console.

## Versions

La version actuelle prends environ 3 heures pour extraire toutes les données du site. Des commits seront apportés pour améliorer ce point. 

## Auteur

**Léo CAPOU** 

## Remerciements

* Tim
