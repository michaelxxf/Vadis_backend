from fastapi import FastAPI
from app.db.session import engine
from app.models import users, drugs, inventory, order_item, support, order  # Add others when ready
from app.routes import auth_routes, drug_routes, inventory_routes, user_routes, ai_routes, order_routes, support_routes # Add others when ready
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
from app.db.base import Base

app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(drug_routes.router)
app.include_router(inventory_routes.router)
app.include_router(user_routes.router)
app.include_router(auth_routes.router)
app.include_router(ai_routes.router)
app.include_router(order_routes.router)
app.include_router(support_routes.router)

