from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from controllers.category_controller import get_all_categories, create_category
from schemas.category import CategoryResponse, CategoryCreate

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse)
def add_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """
    Create a new category in the database.

    This endpoint receives category data, attempts to create the category,
    and returns the created category object.

    Args:
        category (CategoryCreate): Category data to create.
        db (Session, optional): SQLAlchemy database session (injected by Depends).

    Returns:
        CategoryResponse: The newly created category.

    Raises:
        HTTPException: 500 if category creation fails.
    """
    new_category = create_category(db, category)
    if not new_category:
        raise HTTPException(status_code=500, detail="Failed to create category")
    return new_category


@router.get("/get_categories", response_model=list[CategoryResponse])
def fetch_all_categories(db: Session = Depends(get_db)):
    """
    Retrieve all categories from the database.

    Args:
        db (Session, optional): SQLAlchemy database session (injected by Depends).

    Returns:
        list[CategoryResponse]: List of all categories.

    Raises:
        HTTPException: 404 if no categories are found.
    """
    categories = get_all_categories(db)
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found")
    return categories
