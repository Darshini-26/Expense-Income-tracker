from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from service.category_service import CategoryService
from config.database import get_db, SessionLocal
from schemas.schemas import Category, CategoryCreate
from typing import List
from service.unit_of_work import UnitOfWork

router = APIRouter(prefix="/categories", tags=["Category"])

# Dependency to provide a Unit of Work
def get_uow() -> UnitOfWork:
    return UnitOfWork(SessionLocal)

# Create a new Category
@router.post("/", response_model=Category)
def create_category(category: CategoryCreate, uow: UnitOfWork = Depends(get_uow)):
    try:
        return CategoryService.create_category_service(uow, category)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Fetch Category by ID
@router.get("/{category_id}", response_model=Category)
def read_category(category_id: int, uow: UnitOfWork = Depends(get_uow)):
    try:
        return CategoryService.get_category_by_id_service(uow, category_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# Fetch all Categories
@router.get("/", response_model=List[Category])
def read_categories(uow: UnitOfWork = Depends(get_uow)):
    return CategoryService.get_all_categories_service(uow)

# Update Category by ID
@router.put("/{category_id}", response_model=Category)
def update_category(category_id: int, category: CategoryCreate, uow: UnitOfWork = Depends(get_uow)):
    try:
        return CategoryService.update_category_service(uow, category_id, category)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Delete Category by ID
@router.delete("/{category_id}", response_model=dict)
def delete_category(category_id: int, uow: UnitOfWork = Depends(get_uow)):
    try:
        success = CategoryService.delete_category_service(uow, category_id)
        if not success:
            raise HTTPException(status_code=404, detail="Category not found")
        return {"message": "Category deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
