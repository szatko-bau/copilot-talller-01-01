# Compliance Platform

A full-stack web application featuring JWT authentication, built with a FastAPI backend and a React frontend.

---

## Architecture

```
copilot-talller-01-01/
├── backend/          # FastAPI JWT Authentication API
└── frontend/         # React SPA (Login + Welcome pages)
```

---

## Backend

The backend is a **FastAPI** application that provides JWT-based authentication.

### Endpoints

| Method | Path             | Description                             |
|--------|------------------|-----------------------------------------|
| POST   | `/token`         | Login — returns access + refresh tokens |
| POST   | `/token/refresh` | Exchange refresh token for new tokens   |
| GET    | `/me`            | Returns current authenticated user      |

**Default credentials:** `admin` / `admin123`

### Running the backend

#### With Docker Compose (recommended)

```bash
cd backend
docker compose up --build
```

The API will be available at `http://localhost:8000`.

#### With Poetry (local)

```bashasddsadsa
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

Interactive API docs: `http://localhost:8000/docs`

---

## Frontend

A **React** single-page application (Vite) with two protected routes:

- `/login` — Login form that authenticates against the backend
- `/welcome` — Protected dashboard (requires an active session)

The design follows the **Compliance Platform** design system defined in `Compliance-Platform-DESIGN.md`:

- Font: Inter
- Primary colour: `#0F172A` (dark navy)
- Glass-surface aesthetic with subtle shadows
- Grid-based bounded layout with 12 px base rhythm

### Running the frontend

#### Prerequisites

- Node.js 18+

#### Development mode

```bash
cd frontend
npm install
npm run dev
```

The application will open at `http://localhost:5173`.

#### Production build

```bash
cd frontend
npm run build
npm run preview      # serves the built files at http://localhost:4173
```

### Environment variables

Create a `.env.local` file inside the `frontend/` directory if you need to point the app at a different backend URL:

```
VITE_API_URL=http://localhost:8000
```

If the variable is not set, the app defaults to `http://localhost:8000`.

---

## Usage

1. **Start the backend** (see above). It must be running at `http://localhost:8000`.
2. **Start the frontend** in development mode.
3. Open `http://localhost:5173` in your browser — you will be redirected to the **Login** page.
4. Enter the credentials:
   - **Username:** `admin`
   - **Password:** `admin123`
5. Click **Sign in**. On success you are redirected to the **Welcome** dashboard.
6. Click **Sign out** in the top-right corner to end the session and return to the login page.

> **Note:** The authentication token is stored in `sessionStorage`, so it is automatically cleared when you close the browser tab.

---

## Running Tests

### Backend

```bash
cd backend
poetry run pytest tests/ -v
```

---

## Design Reference

See [`Compliance-Platform-DESIGN.md`](./Compliance-Platform-DESIGN.md) for the full design system specification.
