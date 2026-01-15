# Testeur de robustesse de mots de passe

Application full-stack simple pour évaluer la robustesse d'un mot de passe et proposer des phrases de passe fortes. Backend : Flask (Python). Frontend : HTML/CSS/JS.

## Fonctionnalités
- Évalue les mots de passe (longueur, variété des caractères, dictionnaire/séquences, heuristiques de fuites).
- Propose des phrases de passe solides avec séparateurs, chiffres et symboles.
- API REST : POST /api/evaluate, GET /api/suggest, GET /api/health.
- CORS activé pour le développement local du frontend.

## Structure du projet
- app.py — point d'entrée Flask et routage API.
- backend/ — logique d'évaluation (checker.py), utilitaires (utils.py), données de configuration (config.py), routes (routes.py).
- index.html, script.js, style.css — frontend simple pour appeler l'API.

## Pré-requis
- Python 3.10+ recommandé.
- Installation : pip install flask flask-cors

## Lancer le backend
```
python app.py
```
L'API écoute sur http://localhost:5000.

## Lancer le frontend
Ouvrez index.html dans un navigateur (ou servez-le via un serveur statique). Le frontend attend le backend sur http://localhost:5000.

## API
- POST /api/evaluate — corps : { "password": "..." }, renvoie la force, des conseils et des indicateurs.
- GET /api/suggest — renvoie { "suggestion": "passphrase" }.
- GET /api/health — renvoie { "status": "ok" }.

## Notes
- N'utilisez jamais de mots de passe faibles ou déjà compromis.
- En production, placez Flask derrière un vrai serveur (gunicorn/uwsgi) et désactivez le mode debug.
