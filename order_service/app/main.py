from fastapi import FastAPI
from app.database import Base, engine
from app.routers import order_routes
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Order Service")
# Add Prometheus instrumentation
Instrumentator().instrument(app).expose(app)

Base.metadata.create_all(bind=engine)

app.include_router(order_routes.router)

@app.get("/")
def root():
    return {"message": "Order Service is running!"}
