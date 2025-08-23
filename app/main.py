from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import (
    auth_routes,
    admin_routes,
    category_routes,
    negotiation_routes,
    notification_routes,
    order_routes,
    vendor_routes,
)


app = FastAPI(title="Tyda API", version="1.0")


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://negoshop.preview.emergentagent.com",  # si besoin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Autoriser ces origines
    allow_credentials=True,
    allow_methods=["*"],    # Autoriser toutes les méthodes (GET, POST, PUT...)
    allow_headers=["*"],    # Autoriser tous les headers
)
# Register routes
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(admin_routes.router, prefix="/admin", tags=["Admin"])
app.include_router(category_routes.router, prefix="/categories", tags=["Categories"])
app.include_router(negotiation_routes.router, prefix="/negotiations", tags=["Negotiations"])
app.include_router(notification_routes.router, prefix="/notifications", tags=["Notifications"])
app.include_router(order_routes.router, prefix="/orders", tags=["Orders"])
app.include_router(vendor_routes.router, prefix="/vendors", tags=["Vendors"])
