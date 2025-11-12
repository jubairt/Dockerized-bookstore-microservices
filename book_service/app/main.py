from fastapi import FastAPI
from app.routers import book_routes
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.seed_data import seed_books



app = FastAPI(
    title="Book Service",
    description="Handles all book operations",
    version="1.0.0"
)

# Add Prometheus instrumentation
Instrumentator().instrument(app).expose(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(book_routes.router)

@app.get("/")
def root():
    return {"message": "Book service is running!"}

Base.metadata.create_all(bind=engine)
seed_books()