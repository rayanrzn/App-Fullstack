# ai assistant backend

projet api pour un assistant ia avec authentification.

## c'est quoi?

- api fastapi avec login/register
- stocke les users dans users.json
- les conversations dans conversations.json
- utilise openrouter pour l'ia

## setup

```bash
pip install -r requirements.txt
```

créer un fichier `.env`:

```
SECRET_KEY=ta-clé-secrète-bien-longue
LLM_API_KEY=ta-clé-openrouter
LLM_API_URL=https://openrouter.ai/api/v1
LLM_MODEL=meta-llama/llama-3-8b-instruct
DATABASE_DIR=./
```

## lancer le serveur

```bash
python -m uvicorn main:app --reload
```

`http://localhost:8000/docs` pour swagger

## les routes

- `POST /register` - créer un compte
- `POST /login` - se connecter
- `GET /me` - get les infos du user connecté (besoin du token)
- `GET /conversations` - récupérer la conversation du user connecté (besoin du token)
- `POST /chat` - envoyer un msg a l'ia et recevoir la réponse (besoin du token)
- `GET /health` - check si le serveur marche

## comment?

- python 3.13
- fastapi pour l'api
- tinydb pour la db (json)
- bcrypt pour les passwords
- jwt pour les tokens
- openrouter pour l'ia
