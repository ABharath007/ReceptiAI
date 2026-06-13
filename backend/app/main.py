from fastapi import FastAPI
from app.api.routes.business import router as business_router
from app.api.routes.service import router as service_router
from app.api.routes.resource import router as resource_router
from app.api.routes.customer import router as customer_router
from app.api.routes.resource_availability import router as resource_availability_router
from app.api.routes.resource_leave import router as resource_leave_router
from app.api.routes.appointment import router as appointment_router

app = FastAPI(
    title="ReceptiAI",
    version="1.0.0"
)

app.include_router(customer_router)
app.include_router(service_router)
app.include_router(resource_router)
app.include_router(business_router)
app.include_router(resource_availability_router)
app.include_router(resource_leave_router)
app.include_router(appointment_router)
@app.get("/")
def home():
    return {"message": "Welcome to ReceptiAI!"}