from fastapi import APIRouter, HTTPException
from typing import List, Optional
from models.basemodels import Complete_Item_, Item_, Item_Simple_Data_, Item_Tax_Data_, Standard_Output
from models.tables import Item

from services.item_services import add_item_, delete_item_, get_item_, get_simple_item_, update_item_

router = APIRouter(prefix='/items-service')

@router.post('/add-item')
async def add_item(
    item: Item_,
    item_simple_data: Item_Simple_Data_,
    item_tax_data: Item_Tax_Data_):
    return await add_item_(item, item_simple_data, item_tax_data)

@router.post('/update-item', response_model=Standard_Output)
async def update_item(item: Item_, item_simple_data: Item_Simple_Data_, item_tax_data: Item_Tax_Data_):
    return await update_item_(item, item_simple_data, item_tax_data)

@router.get('/get-simple-item', response_model=List[Item_])
async def get_simple_item(
    type_data: str,
    id: int = None,
    name: str = None,
    ean: str = None
):
    match type_data:
        case 'all':
            return await get_simple_item_(type_data, 0)
        case 'id':
            return await get_simple_item_(type_data, id)
        case 'name':
            return await get_simple_item_(type_data, name)
        case 'ean':
            return await get_simple_item_(type_data, ean)
        case _:
            raise HTTPException(status_code=400, detail='O campo data_type não corresponde a um campo válido.')

@router.get('/get-item', response_model=List[Complete_Item_])
async def get_item(
    type_data: str,
    id: int = None,
    name: str = None,
    ean: str = None,
    brand: str = None,
    category: str = None
    ):
    if type_data == 'all':
        return await get_item_(type_data, 0)
    elif type_data == 'id':
        return await get_item_(type_data, id)
    elif type_data == 'name':
        return await get_item_(type_data, name)
    elif type_data == 'ean':
        return await get_item_(type_data, ean)
    elif type_data == 'brand':
        return await get_item_(type_data, brand)
    elif type_data == 'category':
        return await get_item_(type_data, category)
    else:
        raise HTTPException(
            status_code=400,
            detail='O campo type_data não corresponde a um tipo de dado válido.')

@router.delete('/delete-item')
async def delete_item(id: int):
    return await delete_item_(id)