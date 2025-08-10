# echoNest

## Overview
echoNest est un lecteur de musique web local, ultra simple.

### Architecture

Ce lecteur utilise une architecture client/serveur. 

La portion serveur utilise le langage Python avec la librairie FastApi.
Le serveur utilise un cache pour éviter de scanner la structure de répertoire des fichiers musicaux.

La partie client utilise bootstrap, htmx, js.

La configuration de l'application est centralisé dans config.py

### Fonctionnalité

* Affichage des tag mp3 via la librairie EasyID3
* Recherche de musique
* Recherche d'info de la musique en cours via la librairie lyricsgenius
* Gestion de playlist
* Historique de la musique écouté

### Lancement

Lancer l'application et aller dans votre navigateur préféré: http://127.0.0.1:8000/

#### Écran de la bibliothèque

![echoNest library screen](https://raw.githubusercontent.com/marccollin/echonest/master/echoNest_library.jpg)

#### Écran récemment joué

![echoNest library screen](https://raw.githubusercontent.com/marccollin/echonest/master/echoNest_history.jpg)

### Amélioration possible
Utilisation d'une base de donnée ou fichier pour stocker les fichiers scannées et d'éviter de scanner à chaque fois la structure sur le disque.
