from fastapi import FastAPI
from app.database import Base, engine
from app.routers import user_routes
from prometheus_fastapi_instrumentator import Instrumentator

# Create tables if not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service")
# Add Prometheus instrumentation
Instrumentator().instrument(app).expose(app)

app.include_router(user_routes.router)

@app.get("/")
def root():
    return {"message": "User Service is running..."}
