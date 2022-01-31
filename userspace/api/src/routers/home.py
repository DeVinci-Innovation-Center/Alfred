from fastapi import APIRouter
from starlette.responses import RedirectResponse

router = APIRouter(tags=["Home"])


@router.get("/")
async def redirect():
    response = RedirectResponse(url="/docs")
    return response
