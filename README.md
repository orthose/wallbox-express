# Description
**WallboxExpress** est un outil d'aide à la facturation des sessions de recharge effectuées sur les bornes Wallbox.
Cette version de l'outil se veut plus légère par rapport à [wallbox-express-old](https://github.com/orthose/wallbox-express-old).
Elle en reprend l'interface mais n'utilise plus Pandas pour le traitement des données.

Désormais, il est possible d'obtenir la somme de plusieurs indicateurs en filtrant par emplacement et par utilisateur
directement depuis le tableau de bord de l'application web de [Wallbox](https://wallbox.com/fr_fr).
Dès lors, ce projet présente bien moins d'intérêt.

~~Actuellement, il est possible de télécharger le récapitulatif de toutes les sessions de charge effectuées 
pour un mois donné depuis l'interface web de [Wallbox](https://wallbox.com/fr_fr) sous forme d'un fichier CSV.
Cependant, il n'est pas possible de filtrer les utilisateurs ou d'obtenir la somme totale des différents indicateurs
(temps de recharge, énergie consommée et coût financier).~~

**WallboxExpress** est un progamme Python mettant à disposition une interface graphique minimaliste permettant 
de transformer facilement ces données. Son objectif principal est d'éditer automatiquement une facture pré-formattée
sous la forme d'un fichier PDF à partir du coût total des recharges.

# Manuel d'utilisation
Lorsque vous démarrez **WallboxExpress** commencez par charger un fichier en cliquant sur le bouton **Parcourir**.
Un explorateur de fichier s'ouvre et vous pouvez sélectionner le fichier CSV à charger. 
Si le format attendu ne correspond pas une erreur s'affiche. Le programme n'accepte que le format fourni par Wallbox. 
Si le format est correct la table des données s'affiche.

Vous pouvez alors effectuer 4 actions différentes correspondant aux boutons du bas de la fenêtre :
* **Filtrer**: Toutes les lignes de la table dont la case est décochée sont supprimées.
* **Agréger**: Somme les indicateurs par utilisateur au premier appui. Puis de manière globale au second appui.
* **Exporter**: Sauvegarde la table de données sous forme d'un fichier CSV.
* **Facture**: Édite la facture sous forme d'un fichier PDF. La table ne doit contenir qu'une seule ligne.

# Installation
1. Téléchargez la dernière release disponible sur [GitHub](https://github.com/orthose/wallbox-express/releases).
2. Décompressez l'archive ZIP sur le poste client. Si vous êtes sur Windows, 
vous pouvez choisir comme dossier de destination **%LOCALAPPDATA%\Programs**.
3. Configurez le fichier **config.toml** en suivant la section suivante.
4. Lancez l'application en cliquant sur le fichier exécutable **wallbox_express.exe**.

# Configuration
Le seul fichier à configurer est **config.toml**. Il permet de pré-formater la facture. 
Basez-vous sur l'exemple donné par défaut pour le modifier.

La T.V.A. (taxe sur la valeur ajoutée) est un nombre décimal compris entre 0 et 1. 
On considère que le coût donné par Wallbox est le prix T.T.C. (toutes taxes comprises).
Notez que si le fichier est incorrect un message d'erreur sera affiché lors du lancement de l'application.

# Distribution
## Environnement de production
```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Packaging
Les commandes suivantes permettent de créer une archive ZIP distribuable dans le dossier **dist/**.
```shell
pip install pyinstaller
python build_dist.py
```
**Attention :** Le packaging doit s'effectuer sur le système d'exploitation cible. 
PyInstaller n'est pas cross-platform.

# Contribuer
## Environnement de développement
```shell
python -m venv venv
source venv/bin/activate
pip install pip-tools
pip-sync dev-requirements.txt
PYTHONPATH=./src
```
**Astuce :** La variable d'environnement peut être ajoutée dans un fichier **.env** à la racine du projet dans VSCode. 

## Modification des dépendances
```shell
pip-compile dev-requirements.in
pip-compile requirements.in
```

## Exécution des tests
```shell
pytest tests/
```

## Lancement du programme
```shell
python src/wallbox_express.py
```
