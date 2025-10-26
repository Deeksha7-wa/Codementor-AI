from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.submit_code import router
from backend.db.database import init_db

app = FastAPI(title="Codementor AI")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(router)

# --- Create tables on startup ---
@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def root():
    return {"message": "Backend is running!"}




