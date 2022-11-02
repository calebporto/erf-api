from models.basemodels import Person_PF_Data_, Person_PJ_Data_, Standard_Output, Person_
from models.tables import Error_Logs, Person, Person_PF_Data, Person_PJ_Data
from models.connection import async_session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from models.errors import ParamError
from fastapi import HTTPException
from sqlalchemy import delete
from datetime import datetime

async def new_person_pf(new_person, new_person_data):
    async with async_session() as session:
        np, npd = new_person, new_person_data
        if np.doctype == 2:
            raise HTTPException(status_code=400, detail='Tipo de usuário incorreto. Use o endpoint add-person-pj')
        elif np.doctype != 1:
            raise HTTPException(status_code=400, detail='Tipo de usuário incorreto. O campo doctype deve ser 1 ou 2.')
        try:
            # Adicionando person
            session.add(Person(
                np.alternative_id,
                np.name,
                np.email,
                np.user_name,
                np.hash,
                np.doctype,
                np.persontype,
                np.is_active))
            await session.commit()
            
            # Consultando id do 'person' recem adicionado
            id_result = await session.execute(select(Person.id).where(Person.alternative_id == np.alternative_id))
            person_id = id_result.scalars().first()

            # Adicionando person_pf_data
            session.add(
                Person_PF_Data(
                    person_id,
                    npd.cpf,
                    npd.gender,
                    npd.cep,
                    npd.public_place,
                    npd.place_number,
                    npd.complement,
                    npd.district,
                    npd.city,
                    npd.uf,
                    npd.tel,
                    npd.birth
                )
            )
            await session.commit()
            return Standard_Output(message='Operação realizada com sucesso.')
        except Exception as error:
            await session.close()
            
            session.add(Error_Logs(
                str(error), datetime.now(), None, 1, 'add-person-pf'
            ))
            await session.commit()
            
            # Caso a inclusão do person_pf_data dê erro, exclui o person adicionado.
            if 'duplicate key value violates unique constraint "person_pf_data' in str(error):
                id_result = await session.execute(select(Person.id).where(Person.alternative_id == np.alternative_id))
                person_id = id_result.scalars().first()
                await session.execute(delete(Person).where(Person.id == person_id))
                await session.commit()
                raise HTTPException(status_code=400, detail='Já existe usuário com os dados fornecidos.')
            elif 'duplicate key value violates unique constraint "person' in str(error):
                raise HTTPException(status_code=400, detail='Já existe usuário com os dados fornecidos.')
            raise HTTPException(status_code=400, detail='Erro na requisição, verifique os dados.')

async def new_person_pj(new_person, new_person_data):
    async with async_session() as session:
        np, npd = new_person, new_person_data
        if np.doctype == 1:
            raise HTTPException(status_code=400, detail='Tipo de usuário incorreto. Use o endpoint add-person-pf')
        elif np.doctype != 2:
            raise HTTPException(status_code=400, detail='Tipo de usuário incorreto. O campo doctype deve ser 1 ou 2.')
        try:
            # Adicionando person
            session.add(Person(
                np.alternative_id,
                np.name,
                np.email,
                np.user_name,
                np.hash,
                np.doctype,
                np.persontype,
                np.is_active))
            await session.commit()
            
            # Consultando id do 'person' recem adicionado
            id_result = await session.execute(select(Person.id).where(Person.alternative_id == np.alternative_id))
            person_id = id_result.scalars().first()

            # Adicionando person_pj_data
            session.add(
                Person_PJ_Data(
                    person_id,
                    npd.cnpj,
                    npd.cp_name,
                    npd.ie,
                    npd.tel,
                    npd.public_place,
                    npd.place_number,
                    npd.complement,
                    npd.district,
                    npd.city,
                    npd.uf,
                    npd.cep
                )
            )
            await session.commit()
            return Standard_Output(message='Operação realizada com sucesso.')
        except Exception as error:
            await session.close()
            
            session.add(Error_Logs(
                str(error), datetime.now(), None, 1, 'service update_person_pj'
            ))
            await session.commit()
            if 'duplicate key value violates unique constraint "person_pj_data' in str(error):
                id_result = await session.execute(select(Person.id).where(Person.alternative_id == np.alternative_id))
                person_id = id_result.scalars().first()
                await session.execute(delete(Person).where(Person.id == person_id))
                await session.commit()
                raise HTTPException(status_code=400, detail='Já existe usuário com os dados fornecidos.')
            if 'duplicate key value violates unique constraint "person' in str(error):
                raise HTTPException(status_code=400, detail='Já existe usuário com os dados fornecidos.')
            raise HTTPException(status_code=400, detail='Erro na requisição, verifique os dados.')

async def person_pf_update_(person, person_data):
    async with async_session() as session:
        p, pd = person, person_data
        if p.doctype:
            raise HTTPException(status_code=400, detail='Não é possível alterar doctype')
        try:
            result = await session.execute(
                select(Person, Person_PF_Data)
                .join(Person_PF_Data, Person.id == Person_PF_Data.person_id)
                .where(Person.id == p.id))
            
            person_query = result.first()
            
            # p_db = person for database
            # pd_db = person data for database
            p_db, pd_db = person_query[0], person_query[1]


            p_db.alternative_id = p.alternative_id if p.alternative_id else p_db.alternative_id
            p_db.name = p.name if p.name else p_db.name
            p_db.email = p.email if p.email else p_db.email
            p_db.user_name = p.user_name if p.user_name else p_db.user_name
            p_db.hash = p.hash if p.hash else p_db.hash
            p_db.persontype = p.persontype if p.persontype else p_db.persontype
            p_db.is_active = p.is_active if p.is_active else p_db.is_active

            pd_db.cpf = pd.cpf if pd.cpf else pd_db.cpf
            pd_db.gender = pd.gender if pd.gender else pd_db.gender
            pd_db.cep = pd.cep if pd.cep else pd_db.cep
            pd_db.public_place = pd.public_place if pd.public_place else pd_db.public_place
            pd_db.place_number = pd.place_number if pd.place_number else pd_db.place_number
            pd_db.complement = pd.complement if pd.complement else pd_db.complement
            pd_db.district = pd.district if pd.district else pd_db.district
            pd_db.city = pd.city if pd.city else pd_db.city
            pd_db.uf = pd.uf if pd.uf else pd_db.uf
            pd_db.tel = pd.tel if pd.tel else pd_db.tel
            pd_db.birth = pd.birth if pd.birth else pd_db.birth

            session.add(p_db)
            session.add(pd_db)
            await session.commit()
            return Standard_Output(message='Operação efetuada com sucesso.')
        except Exception as error:
            await session.close()
            session.add(Error_Logs(
                str(error), datetime.now(), None, 1, 'service person_pf_update'
            ))
            await session.commit()
            raise HTTPException(status_code=400, detail='Erro na requisição, verifique os dados.')

async def person_pj_update_(person, person_data):
    async with async_session() as session:
        p, pd = person, person_data
        if p.doctype:
            raise HTTPException(status_code=400, detail='Não é possível alterar doctype')
        try:
            result = await session.execute(
                select(Person, Person_PJ_Data)
                .join(Person_PJ_Data, Person.id == Person_PJ_Data.person_id)
                .where(Person.id == p.id))
            
            person_query = result.first()
            
            # p_db = person for database
            # pd_db = person data for database
            p_db, pd_db = person_query[0], person_query[1]


            p_db.alternative_id = p.alternative_id if p.alternative_id else p_db.alternative_id
            p_db.name = p.name if p.name else p_db.name
            p_db.email = p.email if p.email else p_db.email
            p_db.user_name = p.user_name if p.user_name else p_db.user_name
            p_db.hash = p.hash if p.hash else p_db.hash
            p_db.persontype = p.persontype if p.persontype else p_db.persontype
            p_db.is_active = p.is_active if p.is_active else p_db.is_active

            pd_db.cnpj = pd.cnpj if pd.cnpj else pd_db.cnpj
            pd_db.cp_name = pd.cp_name if pd.cp_name else pd_db.cp_name
            pd_db.ie = pd.ie if pd.ie else pd_db.ie
            pd_db.tel = pd.public_place if pd.tel else pd_db.tel
            pd_db.cep = pd.cep if pd.cep else pd_db.cep
            pd_db.public_place = pd.public_place if pd.public_place else pd_db.public_place
            pd_db.place_number = pd.place_number if pd.place_number else pd_db.place_number
            pd_db.complement = pd.complement if pd.complement else pd_db.complement
            pd_db.district = pd.district if pd.district else pd_db.district
            pd_db.city = pd.city if pd.city else pd_db.city
            pd_db.uf = pd.uf if pd.uf else pd_db.uf

            session.add(p_db)
            session.add(pd_db)
            await session.commit()
            return Standard_Output(message='Operação efetuada com sucesso.')
        except Exception as error:
            await session.close()
            session.add(Error_Logs(
                str(error), datetime.now(), None, 1, 'service person_pj_update'
            ))
            await session.commit()
            raise HTTPException(status_code=400, detail='Erro na requisição, verifique os dados.')

async def get_simple_person_(type_data, p_data):
    async with async_session() as session:
        try:
            if type(p_data) == str:
                data = p_data.lower()
            else:
                data = p_data

            if type_data == 'id':
                result = await session.execute(
                    select(Person).where(Person.id == data)
                )
                person = result.scalars().all()
            elif type_data == 'alternative_id':
                result = await session.execute(
                    select(Person).where(Person.alternative_id == data)
                )
                person = result.scalars().all()
            elif type_data == 'name':
                result = await session.execute(
                    select(Person).where(Person.name == data)
                )
                person = result.scalars().all()
            elif type_data == 'email':
                result = await session.execute(
                    select(Person).where(Person.email == data)
                )
                person = result.scalars().all()
            elif type_data == 'user_name':
                result = await session.execute(
                    select(Person).where(Person.user_name == data)
                )
                person = result.scalars().all()
            elif type_data == 'doctype':
                result = await session.execute(
                    select(Person).where(Person.doctype == data)
                )
                person = result.scalars().all()
            else:
                session.add(Error_Logs(
                    'type incorreto', datetime.now(), None, 1, 'service get_simple_person')
                )
                await session.commit()
                raise HTTPException(status_code=400, detail='O campo type está incorreto.')

            for i, item in enumerate(person):
                person_db = Person_(
                    id=item.id,
                    alternative_id=item.alternative_id,
                    name=item.name,
                    email=item.email,
                    user_name=item.user_name,
                    hash=item.hash,
                    doctype=item.doctype,
                    persontype=item.persontype,
                    is_active=item.is_active,
                )
                person[i] = person_db
            return person
        except HTTPException as error:
            raise HTTPException(status_code=error.status_code, detail=error.detail)
        except Exception as error:
            await session.close()
            session.add(Error_Logs(
                str(error), datetime.now(), None, 1, 'service get_simple_person_'
            ))
            await session.commit()
            raise HTTPException(status_code=500, detail='Erro no servidor. Estamos trabalhando para corrigir.')

async def get_pf_data_(type_data, pf_data):
    async with async_session() as session:
        try:
            if type(pf_data) == str:
                data = pf_data.lower()
            else:
                data = pf_data

            if type_data == 'person_id':
                result = await session.execute(
                    select(Person_PF_Data).where(Person_PF_Data.person_id == data)
                )
                person_data = result.scalars().all()
            elif type_data == 'cpf':
                result = await session.execute(
                    select(Person_PF_Data).where(Person_PF_Data.cpf == data)
                )
                person_data = result.scalars().all()
            elif type_data == 'cep':
                result = await session.execute(
                    select(Person_PF_Data).where(Person_PF_Data.cep == data)
                )
                person_data = result.scalars().all()
            elif type_data == 'public_place':
                result = await session.execute(
                    select(Person_PF_Data).where(Person_PF_Data.public_place == data)
                )
                person_data = result.scalars().all()
            elif type_data == 'place_number':
                result = await session.execute(
                    select(Person_PF_Data).where(Person_PF_Data.place_number == data)
                )
                person_data = result.scalars().all()
            elif type_data == 'district':
                result = await session.execute(
                    select(Person_PF_Data).where(Person_PF_Data.district == data)
                )
                person_data = result.scalars().all()
            elif type_data == 'city':
                result = await session.execute(
                    select(Person_PF_Data).where(Person_PF_Data.city == data)
                )
                person_data = result.scalars().all()
            elif type_data == 'uf':
                result = await session.execute(
                    select(Person_PF_Data).where(Person_PF_Data.uf == data)
                )
                person_data = result.scalars().all()
            elif type_data == 'tel':
                result = await session.execute(
                    select(Person_PF_Data).where(Person_PF_Data.tel == data)
                )
                person_data = result.scalars().all()
            elif type_data == 'birth':
                result = await session.execute(
                    select(Person_PF_Data).where(Person_PF_Data.birth == data)
                )
                person_data = result.scalars().all()
            else:
                session.add(Error_Logs(
                    'type incorreto', datetime.now(), None, 1, 'service get_pf_data')
                )
                await session.commit()
                raise HTTPException(status_code=400, detail='O campo type está incorreto.')
            for i, item in enumerate(person_data):
                person_db = Person_PF_Data_(
                    id=item.id,
                    person_id=item.person_id,
                    cpf=item.cpf,
                    gender=item.gender,
                    cep=item.cep,
                    public_place=item.public_place,
                    place_number=item.place_number,
                    complement=item.complement,
                    district=item.district,
                    city=item.city,
                    uf=item.uf,
                    tel=item.tel,
                    birth=item.birth
                )
                person_data[i] = person_db
            return person_data
        except HTTPException as error:
            raise HTTPException(status_code=error.status_code, detail=error.detail)
        except Exception as error:
            await session.close()
            session.add(Error_Logs(
                str(error), datetime.now(), None, 1, 'service get_pf_data_'
            ))
            await session.commit()
            raise HTTPException(status_code=500, detail='Erro no servidor. Estamos trabalhando para corrigir.')

async def get_pj_data_(type_data, pj_data):
    async with async_session() as session:
        try:
            if type(pj_data) == str:
                data = pj_data.lower()
            else:
                data = pj_data
            
            if type_data == 'person_id':
                result = await session.execute(
                    select(Person_PJ_Data).where(Person_PJ_Data.person_id == data)
                )
                person_data = result.scalars().all()
            elif type_data == 'cnpj':
                result = await session.execute(
                    select(Person_PJ_Data).where(Person_PJ_Data.cnpj == data)
                )
                person_data = result.scalars().all()
            elif type_data == 'cp_name':
                result = await session.execute(
                    select(Person_PJ_Data).where(Person_PJ_Data.cp_name == data)
                )
                person_data = result.scalars().all()
            elif type_data == 'ie':
                result = await session.execute(
                    select(Person_PJ_Data).where(Person_PJ_Data.ie == data)
                )
                person_data = result.scalars().all()
            elif type_data == 'tel':
                result = await session.execute(
                    select(Person_PJ_Data).where(Person_PJ_Data.tel == data)
                )
                person_data = result.scalars().all()
            elif type_data == 'cep':
                result = await session.execute(
                    select(Person_PJ_Data).where(Person_PJ_Data.cep == data)
                )
                person_data = result.scalars().all()
            elif type_data == 'public_place':
                result = await session.execute(
                    select(Person_PJ_Data).where(Person_PJ_Data.public_place == data)
                )
                person_data = result.scalars().all()
            elif type_data == 'place_number':
                result = await session.execute(
                    select(Person_PJ_Data).where(Person_PJ_Data.place_number == data)
                )
                person_data = result.scalars().all()
            elif type_data == 'complement':
                result = await session.execute(
                    select(Person_PJ_Data).where(Person_PJ_Data.complement == data)
                )
                person_data = result.scalars().all()
            elif type_data == 'district':
                result = await session.execute(
                    select(Person_PJ_Data).where(Person_PJ_Data.district == data)
                )
                person_data = result.scalars().all()
            elif type_data == 'city':
                result = await session.execute(
                    select(Person_PJ_Data).where(Person_PJ_Data.city == data)
                )
                person_data = result.scalars().all()
            elif type_data == 'uf':
                result = await session.execute(
                    select(Person_PJ_Data).where(Person_PJ_Data.uf == data)
                )
                person_data = result.scalars().all()
            else:
                session.add(Error_Logs(
                    'type incorreto', datetime.now(), None, 1, 'service get_pj_data')
                )
                await session.commit()
                raise HTTPException(status_code=400, detail='O campo type está incorreto.')
            
            for i, item in enumerate(person_data):
                person_db = Person_PJ_Data_(
                    id=item.id,
                    person_id=item.person_id,
                    cnpj=item.cnpj,
                    cp_name=item.cp_name,
                    ie=item.ie,
                    tel=item.tel,
                    cep=item.cep,
                    public_place=item.public_place,
                    place_number=item.place_number,
                    complement=item.complement,
                    district=item.district,
                    city=item.city,
                    uf=item.uf,
                )
                person_data[i] = person_db
            return person_data
        except HTTPException as error:
            raise HTTPException(status_code=error.status_code, detail=error.detail)
        except Exception as error:
            await session.close()
            session.add(Error_Logs(
                str(error), datetime.now(), None, 1, 'get_pj_data_'
            ))
            await session.commit()
            raise HTTPException(status_code=500, detail='Erro no servidor. Estamos trabalhando para corrigir.')

async def delete_person_(doctype, person_id):
    async with async_session() as session:
        try:
            if doctype == 1:
                await session.execute(delete(Person_PF_Data).where(Person_PF_Data.person_id == person_id))
                await session.execute(delete(Person).where(Person.id == person_id))
                await session.commit()
            elif doctype == 2:
                await session.execute(delete(Person_PJ_Data).where(Person_PJ_Data.person_id == person_id))
                await session.execute(delete(Person).where(Person.id == person_id))
                await session.commit()
            else:
                raise HTTPException(status_code=400, detail='O parâmetro "doctype" deve ser 1 ou 2.')
            return Standard_Output(message='Operação realizada com sucesso.')
        except HTTPException as error:
            raise HTTPException(status_code=error.status_code, detail=error.detail)
        except IntegrityError:
            raise HTTPException(status_code=400, detail='Usuário não existe.')
        except Exception as error:
            await session.close()
            session.add(Error_Logs(
                str(error), datetime.now(), None, 1, 'delete_person_'
            ))
            await session.commit()
            raise HTTPException(status_code=500, detail='Erro no servidor. Estamos trabalhando para corrigir.')
