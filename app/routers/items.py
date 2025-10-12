from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/{item_id}")
def get_item(item_id: int):
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("")
def create_item(name: str = Query(..., min_length=1)):
    return {"id": 1, "name": name}
