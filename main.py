from fastapi import FastAPI
from app.routes.orders import router

app = FastAPI(
    title="Trade Orders API",
    description="A FastAPI backend for managing trade orders with WebSocket support.",
    version="1.0.0"
)

app.include_router(router)

# Health check route
@app.get("/")
def home():
    return {"message": "Trade Order System is running"}