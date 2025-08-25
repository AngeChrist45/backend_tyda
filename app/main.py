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
    product_routes
)


app = FastAPI(title="Tyda API", version="1.0")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://frontend-tyda.onrender.com",   # 👈 ton frontend déployé
    "https://negoshop.preview.emergentagent.com"  # 👈 si tu veux tester aussi ici
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Auth"])
app.include_router(admin_routes.router, prefix="/api/admin", tags=["Admin"])
app.include_router(category_routes.router, prefix="/api/categories", tags=["Categors"])
app.include_router(negotiation_routes.router, prefix="/api/negotiations", tags=["Negotiations"])
app.include_router(notification_routes.router, prefix="/api/notifications", tags=["Notifications"])
app.include_router(order_routes.router, prefix="/api/orders", tags=["Orders"])
app.include_router(vendor_routes.router, prefix="/api/vendors", tags=["Vendors"])
app.include_router(product_routes.router, prefix="/api/products", tags=["Products"])
