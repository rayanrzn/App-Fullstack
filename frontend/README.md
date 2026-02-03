# frontend ai assistant

interface react pour l'assistant ia

## c'est quoi?

- interface react avec pages login, register, dashboard, chat
- toutes les pages sensibles sont protegees par jwt
- token stocke en localStorage
- appels au backend en http://localhost:8000

## setup

```bash
npm install
```

lancer en dev:

```bash
npm run dev
```

`http://localhost:5173` pour voir l'app

## structure

```
src/
├── pages/
│   ├── Login.jsx       - page de connexion
│   ├── Register.jsx    - page d'inscription
│   ├── Dashboard.jsx   - infos utilisateur (protegee)
│   └── Chat.jsx        - chatbot ia (protegee)
├── components/
│   ├── ProtectedRoute.jsx  - wrapper de route protegee
│   └── PageFrame.jsx       - layout commun
├── context/
│   └── AuthContext.jsx     - gestion du token jwt
├── App.jsx
└── main.jsx
```

## comment ca marche?

- l'utilisateur se connecte (login/register)
- recoit un token jwt du backend
- token stoke en localStorage
- pour chaque requete au backend, on envoie: `Authorization: Bearer token`
- si token invalide, redirection auto vers /login
- logout supprime le token et redirige vers login

## routes

- `/` → login
- `/login` → page de connexion
- `/register` → page d'inscription
- `/dashboard` → infos user (protegee)
- `/chat` → chatbot ia (protegee)

## appels api

- `POST /register` - creer compte (retourne token)
- `POST /login` - se connecter (retourne token)
- `GET /me` - infos du user connecte (besoin token)
- `GET /conversations` - historique messages (besoin token)
- `POST /chat` - envoyer message ia (besoin token)
