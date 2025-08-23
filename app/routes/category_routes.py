from fastapi import APIRouter
from app.models.category import Category

router = APIRouter()

# Simulé en mémoire
categories = []

@router.post("/")
def create_category(category: Category):
    categories.append(category)
    return {"message": "Category created", "data": category}

@router.get("/")
def list_categories():
    return {"categories": categories}
