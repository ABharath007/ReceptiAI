from fastapi import FastAPI
from app.api.routes.business import router as business_router

app = FastAPI(
    title="ReceptiAI",
    version="1.0.0"
)

app.include_router(business_router)

@app.get("/")
def home():
    return {"message": "Welcome to ReceptiAI!"}