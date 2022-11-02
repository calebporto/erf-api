from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

class Standard_Output(BaseModel):
    message: str

class Person_(BaseModel):
    id: Optional[int] 
    alternative_id: Optional[str] 
    name: Optional[str] 
    email: Optional[str] 
    user_name: Optional[str] 
    hash: Optional[str] 
    doctype: Optional[int] 
    persontype: Optional[list[int]] 
    is_active: Optional[bool]

class Person_PF_Data_(BaseModel):
    id: Optional[int] 
    person_id: Optional[int] 
    cpf: Optional[str] 
    gender: Optional[str] 
    cep: Optional[str] 
    public_place: Optional[str] 
    place_number: Optional[str] 
    complement: Optional[str] 
    district: Optional[str] 
    city: Optional[str] 
    uf: Optional[str] 
    tel: Optional[str] 
    birth: Optional[date] 

class Person_PJ_Data_(BaseModel):
    id: Optional[int]
    person_id: Optional[int]
    cnpj: Optional[str]
    cp_name: Optional[str]
    ie: Optional[str]
    tel: Optional[str]
    cep: Optional[str]
    public_place: Optional[str]
    place_number: Optional[str]
    complement: Optional[str]
    district: Optional[str]
    city: Optional[str]
    uf: Optional[str]

class Item_(BaseModel):
    id: Optional[int]
    name: Optional[str]
    price: Optional[float]
    ean: Optional[str]
    weight: Optional[float]
    inventory: Optional[int]
    is_active: Optional[bool]

class Item_Simple_Data_(BaseModel):
    id: Optional[int]
    item_id: Optional[int]
    cost: Optional[float]
    brand: Optional[str]
    category: Optional[str]
    image_id: Optional[str]

class Item_Tax_Data_(BaseModel):
    id: Optional[int]
    item_id: Optional[int]
    ncm: Optional[str]
    measure: Optional[str]
    origin: Optional[int]
    discount: Optional[float]
    cest: Optional[str]

class Sold_Item_(BaseModel):
    item_id: int
    amount: float
    name: str
    price: float
    weight: float
    ncm: str
    measure: str
    discount: float = None

class Complete_Item_(BaseModel):
    item: Item_
    item_simple_data: Item_Simple_Data_
    item_tax_data: Item_Tax_Data_

class Sale_(BaseModel):
    id: Optional[int]
    client_id: Optional[int]
    salesman_id: Optional[int]
    item_list: Optional[list[Sold_Item_]]
    sale_date: Optional[date]
    total: Optional[float]
    image_id: Optional[str]
    pay_type: Optional[str]
    pay_term: Optional[str]
    is_paid: Optional[bool] = False
    is_delivered: Optional[bool] = False

class Billet_(BaseModel):
    id: Optional[int]
    sale_id: Optional[int]
    value: Optional[float]
    expire_date: Optional[date]
    status: Optional[int]
    transaction_id: Optional[str]
    barcode: Optional[str]
    pixcode: Optional[str]
    billet_link: Optional[str]
    billet_pdf_link: Optional[str]

class Invoice_(BaseModel):
    id: Optional[int]
    sale_id: Optional[int]
    value: Optional[float]
    invoice_datetime: Optional[datetime]
    uuid: Optional[str]
    status: Optional[str]
    nfe_number: Optional[str]
    receipt: Optional[str]
    access_key: Optional[str]
    xml: Optional[str]
    danfe: Optional[str]

class Error_Logs_(BaseModel):
    id: Optional[int]
    log: Optional[str]
    log_datetime: Optional[datetime]
    user_id: Optional[int]
    service_id: Optional[int]
    endpoint: Optional[str]

class Access_(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    access_datetime: Optional[datetime]
    endpoint: Optional[str]

class Permissions_(BaseModel):
    id: Optional[int]
    p_name: Optional[str]
    permission1: Optional[bool]
    permission2: Optional[bool]
    permission3: Optional[bool]
    permission4: Optional[bool]
    permission5: Optional[bool]
    permission6: Optional[bool]
    permission7: Optional[bool]