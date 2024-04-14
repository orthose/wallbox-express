# wallbox-express
WallboxExpress est un outil d'aide à la facturation des sessions de recharge effectuées sur les bornes Wallbox.

```shell
python -m venv venv
source venv/bin/activate
pip install pip-tools
# En cas de modification de dépendances
pip-compile dev-requirements.in
pip-compile requirements.in
# Installation des dépendances en production
pip-sync requirements.txt
# Installation des dépendances en développement
pip-sync dev-requirements.txt
```

```shell
PYTHONPATH=./src
# Exécution des tests automatiques
pytest tests/
# Lancement du programme
python src/run.py
```