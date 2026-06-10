from fastapi import FastAPI
from app.api.routes.business import router as business_router
from app.api.routes.service import router as service_router
from app.api.routes.resource import router as resource_router

app = FastAPI(
    title="ReceptiAI",
    version="1.0.0"
)

app.include_router(service_router)
app.include_router(resource_router)
app.include_router(business_router)

@app.get("/")
def home():
    return {"message": "Welcome to ReceptiAI!"}