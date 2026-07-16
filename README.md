# Beacon

## Run the backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

Backend API: `http://127.0.0.1:8000`  
API docs: `http://127.0.0.1:8000/docs`

## Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Open the URL shown in the terminal (normally `http://localhost:5173`).

