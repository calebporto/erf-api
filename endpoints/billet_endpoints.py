from datetime import date
from typing import List
from fastapi import APIRouter, HTTPException

from models.basemodels import Billet_, Standard_Output
from services.billet_services import billet_register_, billet_update_, get_billet_

router = APIRouter(prefix='/billets-service')

@router.post('/billet-register', response_model=Standard_Output)
async def billet_register(billet_data: Billet_):
    return await billet_register_(billet_data)

@router.post('/billet-update', response_model=Standard_Output)
async def billet_update(billet_data: Billet_):
    return await billet_update_(billet_data)

@router.get('/get-billet', response_model=List[Billet_])
async def get_billet(
    type_data: str,
    id: int = None,
    sale_id: int = None,
    expire_date: date = None,
    status: int = None
):
    '''
    Obtém registros da tabela billet de acordo com os dados fornecidos
    :type_data deve ser id, sale_id, expire_date ou status. Qualquer outro
    campo vai retornar erro.
    '''
    if type_data == 'id':
        return await get_billet_(type_data, id)
    if type_data == 'sale_id':
        return await get_billet_(type_data, sale_id)
    if type_data == 'expire_date':
        return await get_billet_(type_data, expire_date)
    if type_data == 'status':
        return await get_billet_(type_data, status)
    else:
        raise HTTPException(status_code=400, detail='O campo type_data está incorreto')