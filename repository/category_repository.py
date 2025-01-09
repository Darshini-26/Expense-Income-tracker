from sqlalchemy.orm import Session
from models.models import Category

class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        """
        Fetch all income records from the database.

        Returns:
            list: A list of Income objects.
        """
        return self.session.query(Category).all()

    def create_category(self, category: Category) -> Category:
        """Creates a new category in the database."""
        self.session.add(category)
        self.session.commit()  # Commit the transaction to save the category
        self.session.refresh(category)  # Refresh the category to get the generated ID, etc.
        return category

    def get_category_by_id(self, category_id: int) -> Category:
        """Fetches a category by its ID."""
        return self.session.query(Category).filter(Category.category_id == category_id).first()

    def get_all_categories(self):
        """Fetches all categories."""
        return self.session.query(Category).all()

    def get_category_by_name(self, name: str) -> Category:
        """Fetches a category by its name."""
        return self.session.query(Category).filter(Category.name == name).first()

    def update_category(self, category: Category) -> Category:
        """Updates an existing category."""
        self.session.merge(category)  # Merge the updated category into the session
        self.session.commit()  # Commit the transaction to save the changes
        self.session.refresh(category)  # Refresh the category to get the updated data
        return category

    def delete_category(self, category_id: int) -> dict:
        """Deletes a category by its ID."""
        db_category = self.session.query(Category).filter(Category.category_id == category_id).first()
        
        if db_category:
            self.session.delete(db_category)  # Delete the category from the session
            self.session.commit()  # Commit the transaction to finalize the deletion
            return {"message": "Category deleted successfully"}
        
        return {"message": "Category not found"}  # Return a message if no category found
