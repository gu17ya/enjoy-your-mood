from fastapi import APIRouter

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/")
def list_categories():
    return ["Категория 1", "Категория 2"]
