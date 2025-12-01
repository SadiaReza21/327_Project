from sqlalchemy.orm import Session
from models.category import Category
from schemas.category import CategoryCreate

def create_category(db: Session, category: CategoryCreate):
    """
    Create a new category using CategoryCreate schema.
    Returns the created Category object.
    """

    try:
        new_category = Category(
            category_name=category.category_name
        )

        db.add(new_category)
        db.commit()
        db.refresh(new_category)

        return new_category

    except Exception as e:
        db.rollback()
        print("Error creating category:", e)
        return None

def get_all_categories(db: Session):
    """Fetch all categories from the database."""
    try:
        categories = db.query(Category).all()
        return categories
    except Exception as e:
        print("Error fetching categories:", e)
        return []

def get_category_by_id(db: Session, category_id: int):
    """
    Fetch a single category by its ID.
    Returns None if not found.
    """
    return db.query(Category).filter(Category.category_id == category_id).first()


