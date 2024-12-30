from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from service.category_service import CategoryService
from config.database import get_db
from schemas.schemas import Category, CategoryCreate
from typing import List

router = APIRouter(tags=["Category"])

@router.post("/category/", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return CategoryService.create_category_service(db, category)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/category/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    try:
        return CategoryService.get_category_by_id_service(db, category_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/categories/", response_model=List[Category])
def read_categories(db: Session = Depends(get_db)):
    return CategoryService.get_all_categories_service(db)

@router.put("/category/{category_id}", response_model=Category)
def update_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return CategoryService.update_category_service(db, category_id, category)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/category/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    return CategoryService.delete_category_service(db, category_id)
