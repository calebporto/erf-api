from fastapi import APIRouter

from models.basemodels import Access_, Standard_Output
from services.access_services import access_register_

router = APIRouter(prefix='/access-service')

@router.post('/access-register', response_model=Standard_Output)
async def access_register(access_data: Access_):
    return await access_register_(access_data)