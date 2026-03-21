# Smart Workspace

> A unified micro-frontend portal that aggregates multiple applications under a single shell, with Firebase-backed authentication served via a Python Flask REST API.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend Shell | React 18, TypeScript, NX Monorepo, Webpack Module Federation |
| Remote MFEs | auth-app, accounts-app (lazy-loaded remotes) |
| Shared Library | @smart/core — withMVC pattern, Form, TextField, Button |
| State / Forms | react-hook-form, RxJS |
| UI Components | MUI v5, Emotion, Framer Motion, Notistack |
| Auth Backend | Python 3.11, Flask 3, Flask-RESTful, Flask-CORS |
| Auth Provider | Firebase (Pyrebase4) — Email/Password Auth, Realtime DB |
| Hosting | Firebase Hosting + Emulators |
| Containerisation | Docker (gunicorn) |
| Testing | Jest, Vitest, Cypress E2E |
| Tooling | NX 17, pnpm, ESLint, Prettier, SWC |

---

## Architecture Diagram

```mermaid
graph TD
    subgraph Browser
        Shell["smart-workspace\n(NX Host Shell)\nReact + Webpack MF"]
        AuthMFE["auth-app\n(Remote MFE)\nLogin / Register"]
        AccountsMFE["accounts-app\n(Remote MFE)\nAccounts View"]
        CoreLib["@smart/core\n(Shared Lib)\nwithMVC · Form · TextField"]
    end

    subgraph Firebase
        FBAuth["Firebase Auth\n(Email/Password)"]
        FBRTDB["Realtime Database"]
        FBHosting["Firebase Hosting"]
    end

    subgraph AuthService["auth-services (Docker / gunicorn)"]
        Flask["Flask REST API\n/auth/login\n/auth/logout"]
        Pyrebase["Pyrebase4\nFirebase SDK"]
        SessionStore["In-memory\nSession Index"]
    end

    Shell -->|"lazy import()"| AuthMFE
    Shell -->|"lazy import()"| AccountsMFE
    AuthMFE --> CoreLib
    AccountsMFE --> CoreLib

    AuthMFE -->|"POST /auth/login\nPOST /auth/logout\nAxios"| Flask
    Flask --> Pyrebase
    Pyrebase --> FBAuth
    Pyrebase --> FBRTDB
    Flask --> SessionStore

    Shell -->|"deploy"| FBHosting
```

---

## Sequence Diagram — Login Flow

```mermaid
sequenceDiagram
    actor User
    participant Shell as smart-workspace (Shell)
    participant AuthMFE as auth-app (Remote MFE)
    participant Flask as Flask Auth API
    participant Firebase as Firebase Auth

    User->>Shell: Navigate to /auth
    Shell->>AuthMFE: Lazy load auth-app/Module
    AuthMFE-->>User: Render LoginPage (PasswordAuthForm)

    User->>AuthMFE: Submit username + password
    AuthMFE->>Flask: POST /auth/login {username, password}
    Flask->>Firebase: sign_in_with_email_and_password()
    Firebase-->>Flask: idToken + user info
    Flask->>Flask: Store idToken in sessionIndex
    Flask-->>AuthMFE: 200 OK {idToken, ...}

    AuthMFE->>AuthMFE: localStorage.setItem('auth', response)
    AuthMFE-->>User: Snackbar — "Logged in successfully"
    User->>Shell: Navigate to /home
    Shell->>AuthMFE: Load AuthVerifier
    Shell->>AccountsMFE: Lazy load accounts-app/Module
```

---

## Sequence Diagram — Logout Flow

```mermaid
sequenceDiagram
    actor User
    participant AuthMFE as auth-app (Remote MFE)
    participant Flask as Flask Auth API

    User->>AuthMFE: Click Logout
    AuthMFE->>Flask: POST /auth/logout\n(Authorization: bearer <idToken>)
    Flask->>Flask: Extract token from header
    Flask->>Flask: Remove token from sessionIndex
    Flask-->>AuthMFE: 200 OK
    AuthMFE->>AuthMFE: Clear localStorage
```

---

## Database / Firebase ER Diagram

```mermaid
erDiagram
    FIREBASE_USER {
        string uid PK
        string email
        string passwordHash
        string idToken
        timestamp createdAt
        timestamp lastLoginAt
    }

    SESSION_INDEX {
        string idToken PK "in-memory (Flask)"
        object userInfo
        timestamp createdAt
    }

    FIREBASE_REALTIME_DB {
        string projectId PK
        string databaseURL
        string region "asia-southeast1"
    }

    FIREBASE_PROJECT {
        string projectId PK "smart-workspace-e9117"
        string authDomain
        string storageBucket
        string messagingSenderId
        string appId
        string measurementId
    }

    FIREBASE_USER ||--o{ SESSION_INDEX : "idToken stored on login"
    FIREBASE_PROJECT ||--|| FIREBASE_REALTIME_DB : "hosts"
    FIREBASE_PROJECT ||--o{ FIREBASE_USER : "manages"
```

---

## NX Module Federation Map

```mermaid
graph LR
    subgraph NX Workspace
        Shell["apps/smart-workspace\n(Host)"]
        AuthRemote["remotes/auth-app\n(Remote — port 4201)"]
        AccountsRemote["remotes/accounts-app\n(Remote — port 4202)"]
        CoreLib["libs/core\n(@smart/core)"]
        AccountsLib["micro-services/accounts\n(@smart/accounts)"]
    end

    Shell -->|"remotes: ['auth-app','accounts-app']"| AuthRemote
    Shell -->|"remotes: ['auth-app','accounts-app']"| AccountsRemote
    AuthRemote --> CoreLib
    AccountsRemote --> AccountsLib
    AccountsRemote --> CoreLib
```

---

## Project Structure

```
Smart-Workspace/
├── auth-services/          # Python Flask REST API (Docker)
│   └── app/
│       ├── config/         # EnvConfig (firebase keys)
│       ├── db/             # Pyrebase init, session store
│       ├── views/          # /auth/login, /auth/logout
│       ├── utils/          # AuthUtils, StatusGenerator
│       └── models/         # Constants (routes, methods)
└── ui-services/            # NX Monorepo
    ├── apps/smart-workspace/   # Host shell (MF entry)
    ├── remotes/
    │   ├── auth-app/           # Login/Register MFE
    │   └── accounts-app/       # Accounts MFE
    ├── libs/core/              # Shared: withMVC, Form, TextField
    └── micro-services/accounts/ # Accounts component library
```
