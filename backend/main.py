from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.submit_code import router
from backend.db.database import init_db

app = FastAPI(title="Codementor AI")

# --- Allow frontend requests from Render, Vercel, and local dev ---
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://codementor-ai-1.onrender.com",  # your backend (self)
    "https://codementor-ai.vercel.app",      # replace with your Vercel frontend URL
    "*"  # fallback for safety (can remove once your domain is fixed)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include routes ---
app.include_router(router)

# --- Database setup on startup ---
@app.on_event("startup")
def startup_event():
    init_db()

# --- Health check endpoint ---
@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"message": "Backend is running!"}

