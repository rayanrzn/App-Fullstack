# ai assistant

application fullstack avec authentification jwt et chatbot ia

## c'est quoi?

- backend fastapi qui gere l'auth et appelle l'ia
- frontend react avec pages protegees par jwt
- stockage json pour users et conversations
- appel ia via openrouter

## tech

- backend: fastapi + uvicorn + tinydb
- frontend: react + vite + react-router
- auth: jwt + bcrypt
- llm: openrouter

## installation

### backend

```bash
cd backend
pip install -r requirements.txt
```

creer un fichier `.env`:

```
SECRET_KEY=azertyuiopqsdfghjklmwxcvbn1234567890
LLM_API_KEY=ta-clé-openrouter
LLM_API_URL=https://openrouter.ai/api/v1
LLM_MODEL=meta-llama/llama-3-8b-instruct
DATABASE_DIR=./
```

lancer:

```bash
python -m uvicorn main:app --reload
```

`http://localhost:8000/docs` pour swagger

### frontend

```bash
cd frontend
npm install
npm run dev
```

`http://localhost:5173` pour voir l'app

## structure du projet

```
.
├── backend/
│   ├── main.py           - toutes les routes api
│   ├── auth.py           - jwt + bcrypt
│   ├── database.py       - tinydb users/conversations
│   ├── models.py         - pydantic models
│   ├── config.py         - config depuis .env
│   ├── requirements.txt
│   ├── users.json        - db users
│   ├── conversations.json - db conversations
│   ├── .env.example
│   └── README.md
│
└── frontend/
    ├── src/
    │   ├── pages/        - login, register, dashboard, chat
    │   ├── components/   - protectedroute, pageframe
    │   ├── context/      - authcontext (gestion jwt)
    │   ├── App.jsx
    │   └── main.jsx
    ├── package.json
    ├── vite.config.js
    ├── README.md
    └── index.html
```

## routes api

### publiques (sans token)

- `POST /register` - creer compte
- `POST /login` - se connecter
- `GET /health` - check serveur

### protegees (besoin token jwt)

- `POST /logout` - se deconnecter
- `GET /me` - infos du user
- `GET /conversations` - historique messages
- `POST /chat` - envoyer message ia

## comment ca marche?

### inscription

```
utilisateur → register → backend cree user + hash password
→ genere token jwt → envoie token au frontend
→ frontend stocke en localStorage
```

### connexion

```
utilisateur → login → backend verifie email/password
→ genere token jwt → envoie token au frontend
→ frontend stocke en localStorage
```

### chat

```
utilisateur → envoie message → frontend ajoute jwt au header
→ backend verifie jwt → appelle openrouter → sauvegarde en db
→ renvoie reponse ia au frontend
```

### deconnexion

```
utilisateur → logout → frontend supprime token de localStorage
→ redirection vers login
```

## points cles

- **jwt protege les routes** - backend verifie le token sur /me, /conversations, /chat
- **password hashé** - bcrypt rend les mots de passe non lisibles
- **token en localStorage** - persiste la session du user
- **routes protegees frontend** - ProtectedRoute verifie si token existe
- **appel ia backend only** - clé api jamais exposee au frontend
- **historique par user** - chaque user a sa conversation

## openrouter

1. s'inscrire: https://openrouter.ai
2. creer clé api: https://openrouter.ai/keys
3. copier dans `.env`:

```
LLM_API_KEY=sk-or-...ta-clé...
```

modeles gratuits:
- meta-llama/llama-3-8b-instruct
- gpt-3.5-turbo
- mistralai/mistral-7b-instruct

## commits git

```
feat: register + login avec jwt
feat: bcrypt password hashing
feat: protected routes avec jwt
feat: chat interface with ai
feat: database schema users/conversations
docs: add readme et configuration
```
