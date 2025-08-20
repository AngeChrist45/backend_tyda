from fastapi import FastAPI
from routes import (
    auth_routes,
    admin_routes,
    category_routes,
    negotiation_routes,
    notification_routes,
    order_routes,
    vendor_routes,
)

app = FastAPI(title="Tyda API", version="1.0")

# Register routes
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(admin_routes.router, prefix="/admin", tags=["Admin"])
app.include_router(category_routes.router, prefix="/categories", tags=["Categories"])
app.include_router(negotiation_routes.router, prefix="/negotiations", tags=["Negotiations"])
app.include_router(notification_routes.router, prefix="/notifications", tags=["Notifications"])
app.include_router(order_routes.router, prefix="/orders", tags=["Orders"])
app.include_router(vendor_routes.router, prefix="/vendors", tags=["Vendors"])
