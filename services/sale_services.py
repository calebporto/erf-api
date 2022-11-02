from models.basemodels import Sale_, Sold_Item_, Standard_Output
from models.tables import Billet, Invoice, Sale, Error_Logs
from sqlalchemy.exc import IntegrityError, DBAPIError
from models.connection import async_session
from models.errors import ParamError
from sqlalchemy.future import select
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import delete
from json import dumps, loads


recursive_count = 0

async def add_sale_(sale_data):
    async with async_session() as session:
        try:
            # Transformando objetos pydantic em dicionários, para depois
            # converter para json
            for i, item in enumerate(sale_data.item_list):
                data = item.dict()
                (sale_data.item_list)[i] = data

            session.add(Sale(
                client_id=sale_data.client_id,
                salesman_id=sale_data.salesman_id,
                item_list=dumps(sale_data.item_list),
                sale_date=sale_data.sale_date,
                total=sale_data.total,
                image_id=sale_data.image_id,
                pay_type=sale_data.pay_type,
                pay_term=sale_data.pay_term,
                is_paid=sale_data.is_paid,
                is_delivered=sale_data.is_delivered
            ))
            await session.commit()
            return Standard_Output(message='Operação realizada com sucesso.')
        except IntegrityError:
            raise HTTPException(status_code=400, detail='Erro na requisição. Verifique os dados e tente novamente.')
        except Exception as error:
            await session.close()
            session.add(Error_Logs(
                str(error), datetime.now(), None, 1, 'service add_sale_'
            ))
            await session.commit()
            raise HTTPException(status_code=500, detail='Erro interno do servidor. Estamos trabalhando para corrigir.')

async def update_sale_(sale_data):
    async with async_session() as session:
        try:
            result = await session.execute(
                select(Sale).where(Sale.id == sale_data.id)
            )
            sale_db = result.scalars().first()

            if sale_data.item_list:
                for i, item in enumerate(sale_data.item_list):
                    data = item.dict()
                    (sale_data.item_list)[i] = data
                sale_db.item_list = sale_data.item_list
            sale_db.client_id = sale_data.client_id if sale_data.client_id else sale_db.client_id
            sale_db.salesman_id = sale_data.salesman_id if sale_data.salesman_id else sale_db.salesman_id
            sale_db.sale_date = sale_data.sale_date if sale_data.sale_date else sale_db.sale_date
            sale_db.total = sale_data.total if sale_data.total else sale_db.total
            sale_db.image_id = sale_data.image_id if sale_data.image_id else sale_db.image_id
            sale_db.pay_type = sale_data.pay_type if sale_data.pay_type else sale_db.pay_type
            sale_db.pay_term = sale_data.pay_term if sale_data.pay_term else sale_db.pay_term
            sale_db.is_paid = sale_data.is_paid if sale_data.is_paid else sale_db.is_paid
            sale_db.is_delivered = sale_data.is_delivered if sale_data.is_delivered else sale_db.is_delivered

            session.add(sale_db)
            await session.commit()
            return Standard_Output(message='Operação realizada com sucesso.')
        except IntegrityError:
            raise HTTPException(status_code=400, detail='Erro na requisição. Verifique os dados e tente novamente.')
        except DBAPIError:
            raise HTTPException(status_code=400, detail='Erro na requisição. Verifique os dados e tente novamente.')
        except Exception as error:
            await session.close()
            session.add(Error_Logs(
                str(error), datetime.now(), None, 1, 'service update_sale_'
            ))
            await session.commit()
            raise HTTPException(status_code=500, detail='Erro interno do servidor. Estamos trabalhando para corrigir.')

async def get_sale_(type_data, sale_data):
    async with async_session() as session:
        try:
            if type_data == 'id':
                result = await session.execute(select(Sale).where(Sale.id == sale_data))
                sale_db = result.scalars().all()
            elif type_data == 'client_id':
                result = await session.execute(select(Sale).where(Sale.client_id == sale_data))
                sale_db = result.scalars().all()
            elif type_data == 'salesman_id':
                result = await session.execute(select(Sale).where(Sale.salesman_id == sale_data))
                sale_db = result.scalars().all()
            elif type_data == 'sale_date':
                result = await session.execute(select(Sale).where(Sale.sale_date == sale_data))
                sale_db = result.scalars().all()
            elif type_data == 'pay_type':
                result = await session.execute(select(Sale).where(Sale.pay_type == sale_data))
                sale_db = result.scalars().all()
            elif type_data == 'pay_term':
                result = await session.execute(select(Sale).where(Sale.pay_term == sale_data))
                sale_db = result.scalars().all()
            elif type_data == 'is_paid':
                result = await session.execute(select(Sale).where(Sale.is_paid == sale_data))
                sale_db = result.scalars().all()
            elif type_data == 'is_delivered':
                result = await session.execute(select(Sale).where(Sale.is_delivered == sale_data))
                sale_db = result.scalars().all()
            else:
                raise ParamError(status_code=400, detail='O campo type_data não corresponde a um campo válido.')
            
            
            for i, item in enumerate(sale_db):
                # Convertendo item_list de json em lista de dicionarios
                item_list = loads(item.item_list)
                for x, item2 in enumerate(item_list):
                    # Convertendo dicionários em objetos Sold_Item_
                    data2 = Sold_Item_(**item2)
                    item_list[x] = data2

                data = Sale_(
                    id=item.id,
                    client_id=item.client_id,
                    salesman_id=item.salesman_id,
                    item_list=item_list,
                    sale_date=item.sale_date,
                    total=item.total,
                    image_id=item.image_id,
                    pay_type=item.pay_type,
                    pay_term=item.pay_term,
                    is_paid=item.is_paid,
                    is_delivered=item.is_delivered
                )
                sale_db[i] = data
            return sale_db
        except IntegrityError:
            raise HTTPException(status_code=400, detail='Erro na requisição. Verifique os dados e tente novamente.')
        except DBAPIError:
            raise HTTPException(status_code=400, detail='Erro na requisição. Verifique os dados e tente novamente.')
        except Exception as error:
            await session.close()
            session.add(Error_Logs(
                str(error), datetime.now(), None, 1, 'service get_sale_'))

async def sale_delete_(id):
    async with async_session() as session:
        global recursive_count
        try:
            await session.execute(delete(Billet).where(Billet.sale_id == id))
            await session.execute(delete(Invoice).where(Invoice.sale_id == id))
            await session.execute(delete(Sale).where(Sale.id == id))
            await session.commit()
            return Standard_Output(message='Operação efetuada com sucesso.')
        except Exception as error:
            result = await session.execute(select(Billet).where(Billet.sale_id == id))
            billet_db = result.scalars().all()
            if len(billet_db) > 0 and recursive_count < 3:
                recursive_count +=1
                await sale_delete_(id)
            
            result = await session.execute(select(Invoice).where(Invoice.sale_id == id))
            invoice_db = result.scalars().all()
            if len(invoice_db) > 0 and recursive_count < 3:
                recursive_count +=1
                await sale_delete_(id)
            
            result = await session.execute(select(Sale).where(Sale.id == id))
            sale_db = result.scalars().all()
            if len(sale_db) > 0 and recursive_count < 3:
                recursive_count +=1
                await sale_delete_(id)
            raise HTTPException(status_code=500, detail='Erro interno do servidor. Estamos trabalhando para corrigir.')
