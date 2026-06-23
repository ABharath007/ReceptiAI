from fastapi import FastAPI
from app.api.routes.business import router as business_router
from app.api.routes.service import router as service_router
from app.api.routes.resource import router as resource_router
from app.api.routes.customer import router as customer_router
from app.api.routes.resource_availability import router as resource_availability_router
from app.api.routes.resource_leave import router as resource_leave_router
from app.api.routes.appointment import router as appointment_router
from app.api.routes.scheduling import router as scheduling_router
from app.api.routes.ticket import router as ticket_router
from app.api.routes.knowledge_base import router as knowledge_base_router
from app.api.routes.resource_service import router as resource_service_router

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
app.include_router(scheduling_router)
app.include_router(ticket_router)
app.include_router(knowledge_base_router)
app.include_router(resource_service_router)
@app.get("/")
def home():
    return {"message": "Welcome to ReceptiAI!"}