from typing import Optional
from fastapi import APIRouter

router = APIRouter(prefix='/invoices-service')

@router.post('/invoice-generate')
async def invoice_generate(invoice_data):
    pass

@router.get('/get-invoice')
async def get_invoice(id: Optional[int], period: Optional[list]):
    '''
    Consulta nota fiscal por id ou por período, que deve ser uma lista com dois itens,
    a data de início e a data final do período. Caso a lista venha com mais de 2 itens, será
    retornado um erro 402.
    '''
    pass