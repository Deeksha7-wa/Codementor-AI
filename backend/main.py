from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.submit_code import router
from backend.db.database import init_db

app = FastAPI(title="Codementor AI")

# --- Allow frontend requests from Render, Vercel, and local dev ---
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://codementor-ai-1.onrender.com",  # your backend (Render)
    "https://codementor-ai.vercel.app",      # your frontend (Vercel)
    "*",  # fallback (optional)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include API routes ---
app.include_router(router)

# --- Startup: Initialize DB only ---
@app.on_event("startup")
def startup_event():
    init_db()

# --- Health check endpoint (for Render ping) ---
@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"message": "Backend is running!"}

