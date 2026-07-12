
# Modular AI Backend (FastAPI, API-only)

## Struktur
```
app/
├── main.py              # Entry point, CORS, exception handlers global
├── core/
│   ├── config.py        # Settings dari .env
│   └── database.py      # Engine & session async SQLAlchemy
├── models/              # ORM (User, ActivityLog, AIInferenceLog)
├── schemas/             # Pydantic (validasi & envelope respons)
├── routers/             # Endpoint HTTP (tipis, delegasi ke services)
└── services/            # Logika bisnis, AI engine, agregasi
```

## Menjalankan
```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
# Swagger: http://localhost:8000/docs
```

## Format respons (semua endpoint)
```json
{ "status": "success", "message": "OK", "data": { ... } }
```

## Contoh integrasi frontend (Fetch API)
```js
// Toggle mode anonim
await fetch("http://localhost:8000/api/v1/user/privacy?user_id=1", {
  method: "PATCH",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ is_anonymous: true }),
});

// Inferensi AI
const res = await fetch("http://localhost:8000/api/v1/ai/generate", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ user_id: 1, prompt: "Halo!", max_tokens: 256 }),
});
const { status, data } = await res.json();

// Dashboard
const stats = await fetch("http://localhost:8000/api/v1/dashboard/stats")
  .then(r => r.json());
```

## Catatan produksi
- Ganti query param `user_id` dengan autentikasi (JWT/OAuth2) — struktur sudah siap: cukup ganti dependency di router.
- Gunakan Alembic untuk migrasi (init_db create_all hanya untuk dev).
- Set `DATABASE_URL` ke PostgreSQL + asyncpg.

# Desa-Gk-Pake-Dollar

