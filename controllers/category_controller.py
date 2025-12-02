from sqlalchemy.orm import Session
from models.category import Category
from schemas.category import CategoryCreate


def create_category(db: Session, category: CategoryCreate):
    """
    Create a new category in the database.

    Args:
        db (Session): SQLAlchemy database session.
        category (CategoryCreate): Data required to create a new category.

    Returns:
        Category | None: The newly created Category object, or None if an error occurred.
    """

    try:
        new_category = Category(category_name=category.category_name)

        db.add(new_category)
        db.commit()
        db.refresh(new_category)

        return new_category

    except Exception as e:
        db.rollback()
        print("Error creating category:", e)
        return None


def get_all_categories(db: Session):
    """
    Retrieve all categories from the database.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        list[Category]: List of all Category objects. Returns an empty list if an error occurs.
    """
    try:
        categories = db.query(Category).all()
        return categories
    except Exception as e:
        print("Error fetching categories:", e)
        return []


def get_category_by_id(db: Session, category_id: int):
    """
    Retrieve a single category by its ID.

    Args:
        db (Session): SQLAlchemy database session.
        category_id (int): ID of the category to fetch.

    Returns:
        Category | None: Category object if found, else None.
    """
    return db.query(Category).filter(Category.category_id == category_id).first()
