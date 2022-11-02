from fastapi import APIRouter

router = APIRouter(prefix='/access-service')

@router.get('/')
async def home():
    return 'access-service'