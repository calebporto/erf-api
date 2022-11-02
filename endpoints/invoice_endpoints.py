from services.invoice_services import invoice_register_, invoice_update_, get_invoice_
from models.basemodels import Invoice_, Standard_Output
from fastapi import HTTPException
from datetime import datetime
from fastapi import APIRouter
from typing import List


router = APIRouter(prefix='/invoices-service')

@router.post('/invoice-register', response_model=Standard_Output)
async def invoice_register(invoice_data: Invoice_):
    '''
    Registra os dados de uma nota fiscal emitida na API,
    de acordo com os dados retornados pela receita
    '''
    return await invoice_register_(invoice_data)

@router.post('/invoice-update', response_model=Standard_Output)
async def invoice_update(invoice_data: Invoice_):
    '''
    Altera os dados registrados de uma nota fiscal
    '''
    return await invoice_update_(invoice_data)

@router.get('/get-invoice', response_model=List[Invoice_])
async def get_invoice(
    type_data: str,
    id: int = None,
    sale_id: int = None,
    invoice_datetime: datetime = None,
    status: str = None
):
    '''
    Obtém dados de uma nota fiscal registrada no banco de dados

    :type_data é o campo a ser consultado da nota fiscal, e deve ser:
    - id: int
    - sale_id: int
    - invoice_datetime: datetime
    - status: str
    Qualquer campo diferente retorna um erro.
    '''
    if type_data == 'id':
        return await get_invoice_(type_data, id)
    elif type_data == 'sale_id':
        return await get_invoice_(type_data, sale_id)
    elif type_data == 'invoice_datetime':
        return await get_invoice_(type_data, invoice_datetime)
    elif type_data == 'status':
        return await get_invoice_(type_data, status)
    else:
        raise HTTPException(status_code=400, detail='O campo type_data não corresponde a um campo válido.')