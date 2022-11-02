from services.person_services import *
from models.basemodels import Person_, Person_PF_Data_, Person_PJ_Data_, Standard_Output
from fastapi import APIRouter
from datetime import date
from typing import List


router = APIRouter(prefix='/persons-service')

@router.post('/add-person-pf')
async def add_person_pf(new_person: Person_, new_person_data: Person_PF_Data_):
    return await new_person_pf(new_person, new_person_data)

@router.post('/add-person-pj')
async def add_person_pj(new_person: Person_, new_person_data: Person_PJ_Data_):
    return await new_person_pj(new_person, new_person_data)

@router.post('/update-person-pf')
async def update_person_pf(person: Person_, person_pf_data: Person_PF_Data_):
    await person_pf_update(person, person_pf_data)

@router.get('/get-simple-person', response_model=List[Person_])
async def get_simple_person(
    type_data: str,
    id: int = None,
    alternative_id: str = None,
    name: str = None,
    email: str = None,
    user_name: str = None,
    doctype: int = None):

    if id:
        return await get_simple_person_(type_data, id)
    if alternative_id:
        return await get_simple_person_(type_data, alternative_id)
    if name:
        return await get_simple_person_(type_data, name)
    if email:
        return await get_simple_person_(type_data, email)
    if user_name:
        return await get_simple_person_(type_data, user_name)
    if doctype:
        return await get_simple_person_(type_data, doctype)

@router.get('/get-pf-data', response_model=List[Person_PF_Data_])
async def get_pf_data(
    type_data: str,
    id: int = None,
    person_id: int = None,
    cpf: str = None,
    gender: str = None,
    cep: str = None,
    public_place: str = None,
    place_number: str = None,
    complement: str = None,
    district: str = None,
    city: str = None,
    uf: str = None,
    tel: str = None,
    birth: date = None
    ):
    if id:
        return await get_pf_data_(type_data, id)
    if person_id:
        return await get_pf_data_(type_data, person_id)
    if cpf:
        return await get_pf_data_(type_data, cpf)
    if gender:
        return await get_pf_data_(type_data, gender)
    if cep:
        return await get_pf_data_(type_data, cep)
    if public_place:
        return await get_pf_data_(type_data, public_place)
    if place_number:
        return await get_pf_data_(type_data, place_number)
    if complement:
        return await get_pf_data_(type_data, complement)
    if district:
        return await get_pf_data_(type_data, district)
    if city:
        return await get_pf_data_(type_data, city)
    if uf:
        return await get_pf_data_(type_data, uf)
    if tel:
        return await get_pf_data_(type_data, tel)
    if birth:
        return await get_pf_data_(type_data, birth)

@router.get('/get-pj-data', response_model=List[Person_PJ_Data_])
async def get_pf_data(
    type_data: str,
    id: int = None,
    person_id: int = None,
    cnpj: str = None,
    cp_name: str = None,
    ie: str = None,
    tel: str = None,
    cep: str = None,
    public_place: str = None,
    place_number: str = None,
    complement: str = None,
    district: str = None,
    city: str = None,
    uf: str = None
    ):
    if id:
        return await get_pj_data_(type_data, id)
    if person_id:
        return await get_pj_data_(type_data, person_id)
    if cnpj:
        return await get_pj_data_(type_data, cnpj)
    if cp_name:
        return await get_pj_data_(type_data, cp_name)
    if ie:
        return await get_pj_data_(type_data, ie)
    if tel:
        return await get_pj_data_(type_data, tel)
    if cep:
        return await get_pj_data_(type_data, cep)
    if public_place:
        return await get_pj_data_(type_data, public_place)
    if place_number:
        return await get_pj_data_(type_data, place_number)
    if complement:
        return await get_pj_data_(type_data, complement)
    if district:
        return await get_pj_data_(type_data, district)
    if city:
        return await get_pj_data_(type_data, city)
    if uf:
        return await get_pj_data_(type_data, uf)

@router.delete('/delete-person', response_model=Standard_Output)
async def delete_person(doctype: int, person_id: int):
    return await delete_person_(doctype, person_id)