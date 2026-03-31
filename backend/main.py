# backend/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api import routes_ingest, routes_chat

# -----------------------
# Initialize FastAPI app
# -----------------------
app = FastAPI(title="RAG Backend")

# -----------------------
# CORS (needed if frontend served separately or deployed)
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Include Routers
# -----------------------
app.include_router(routes_ingest.router)
app.include_router(routes_chat.router)

# -----------------------
# Serve frontend
# -----------------------
# Path to the frontend folder (relative to this main.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")

# Serve static files (CSS/JS/images if you have any)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# Serve index.html at root
@app.get("/")
def serve_index():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "index.html not found"}

# -----------------------
# Health check endpoint
# -----------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}