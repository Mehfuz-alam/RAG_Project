from fastapi import FastAPI
from app.api import routes_ingest, routes_chat

# ✅ DB setup
from app.db.base import Base
from app.db.session import engine
from app.db import models  # VERY IMPORTANT (registers tables)

app = FastAPI(title="RAG Backend")

# ✅ CREATE TABLES HERE (only place)
Base.metadata.create_all(bind=engine)

# Routes
app.include_router(routes_ingest.router)
app.include_router(routes_chat.router)