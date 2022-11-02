from services.sale_services import add_sale_, get_sale_, sale_delete_, update_sale_
from models.basemodels import Sale_, Standard_Output
from fastapi import APIRouter
from datetime import date


router = APIRouter(prefix='/sales-service')

@router.post('/add-sale', response_model=Standard_Output)
async def add_sale(sale_data: Sale_):
    return await add_sale_(sale_data)

@router.post('/update-sale', response_model=Standard_Output)
async def update_sale(sale_data: Sale_):
    return await update_sale_(sale_data)

@router.get('/get-sale')
async def get_sale(
    type_data: str,
    id: int = None,
    client_id: int = None,
    salesman_id: int = None,
    sale_date: date = None,
    pay_type: str = None,
    pay_term: str = None,
    is_paid: bool = None,
    is_delivered: bool = None
    ):
    if type_data == 'id':
        return await get_sale_(type_data, id)
    if type_data == 'client_id':
        return await get_sale_(type_data, client_id)
    if type_data == 'salesman_id':
        return await get_sale_(type_data, salesman_id)
    if type_data == 'sale_date':
        return await get_sale_(type_data, sale_date)
    if type_data == 'pay_type':
        return await get_sale_(type_data, pay_type)
    if type_data == 'pay_term':
        return await get_sale_(type_data, pay_term)
    if type_data == 'is_paid':
        return await get_sale_(type_data, is_paid)
    if type_data == 'is_delivered':
        return await get_sale_(type_data, is_delivered)
    
@router.get('/sale-delete', response_model=Standard_Output)
async def sale_delete(id: int):
    return await sale_delete_(id)