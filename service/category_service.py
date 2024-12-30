from sqlalchemy.orm import Session
from fastapi import HTTPException
from repository.category_repository import CategoryRepository
from schemas.schemas import CategoryCreate
from models.models import Category

class CategoryService:
    @staticmethod
    def create_category_service(db: Session, category: CategoryCreate) -> Category:
        db_category = Category(name=category.name, description=category.description)
        return CategoryRepository.create_category(db, db_category)

    @staticmethod
    def get_category_by_id_service(db: Session, category_id: int) -> Category:
        category = CategoryRepository.get_category_by_id(db, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    @staticmethod
    def get_all_categories_service(db: Session):
        return CategoryRepository.get_all_categories(db)

    @staticmethod
    def update_category_service(db: Session, category_id: int, category: CategoryCreate) -> Category:
        db_category = db.query(Category).filter(Category.category_id == category_id).first()
        if not db_category:
            raise HTTPException(status_code=404, detail="Category not found")

        db_category.name = category.name
        db_category.description = category.description

        return CategoryRepository.update_category(db, db_category)

    @staticmethod
    def delete_category_service(db: Session, category_id: int):
        result = CategoryRepository.delete_category(db, category_id)
        if not result:
            raise HTTPException(status_code=404, detail="Category not found")
        return result
