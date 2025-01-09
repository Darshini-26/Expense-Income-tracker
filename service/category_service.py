from fastapi import HTTPException
from models.models import Category
from repository.category_repository import CategoryRepository
from schemas.schemas import CategoryCreate
from .unit_of_work import UnitOfWork


class CategoryService:
    @staticmethod
    def create_category_service(uow: UnitOfWork, category: CategoryCreate) -> Category:
        """Handles business logic for creating a new category."""
        with uow:
            # Check for duplicate category names using the repository
            existing_category = uow.categories.get_category_by_name(category.name)
            if existing_category:
                raise HTTPException(status_code=400, detail="Category with this name already exists")

            # Prepare Category object
            db_category = Category(name=category.name, description=category.description)

            # Use repository to create category
            created_category = uow.categories.create_category(db_category)

            uow.commit()  # Commit the transaction after creation
            return created_category

    @staticmethod
    def get_category_by_id_service(uow: UnitOfWork, category_id: int) -> Category:
        """Handles business logic for fetching a category by ID."""
        with uow:
            # Access the repository to fetch category by ID
            category = uow.categories.get_category_by_id(category_id)
            if not category:
                raise HTTPException(status_code=404, detail="Category not found")
            return category

    @staticmethod
    def get_all_categories_service(uow: UnitOfWork):
        """Handles business logic for fetching all categories."""
        with uow:
            # Fetch all categories using the repository
            categories = uow.categories.get_all_categories()
            return categories

    @staticmethod
    def update_category_service(uow: UnitOfWork, category_id: int, category: CategoryCreate) -> Category:
        """Handles business logic for updating a category."""
        with uow:
            # Fetch category to be updated
            db_category = uow.categories.get_category_by_id(category_id)
            if not db_category:
                raise HTTPException(status_code=404, detail="Category not found")

            # Update the category fields
            db_category.name = category.name
            db_category.description = category.description

            # Use the repository to update the category
            updated_category = uow.categories.update_category(db_category)
            return updated_category

    @staticmethod
    def delete_category_service(uow: UnitOfWork, category_id: int):
        """Handles business logic for deleting a category."""
        with uow:
            # Use repository to delete category
            success = uow.categories.delete_category(category_id)
            if not success:
                raise HTTPException(status_code=404, detail="Category not found")

            uow.commit()  # Commit the transaction after deletion
            return {"message": "Category deleted successfully"}
