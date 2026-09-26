from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from dependencies.db_dependency import get_db
from schemas.schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from services.services import CategoryService

router = APIRouter(prefix="/api/categories", tags=["Categories"])
category_service = CategoryService()

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(schema: CategoryCreate, db: Session = Depends(get_db)):
    return category_service.create(db, schema)

@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return category_service.get_all(db)

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    return category_service.get_by_id(db, category_id)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, schema: CategoryUpdate, db: Session = Depends(get_db)):
    return category_service.update(db, category_id, schema)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    force_delete: bool = Query(False, description="Force delete category and associated todos"),
    db: Session = Depends(get_db)
):
    category_service.delete(db, category_id, force_delete=force_delete)
    return None