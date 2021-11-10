from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_index():
    return {"message": "Welcome to ALFRED's dashboard."}


@router.get("/hello")
async def hello_world():
    return {"message": "Hello World"}
