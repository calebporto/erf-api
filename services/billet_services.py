from datetime import datetime
from fastapi import HTTPException
from models.basemodels import Billet_, Standard_Output
from models.connection import async_session
from models.tables import Billet, Error_Logs
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.future import select

async def billet_register_(billet_data):
    async with async_session() as session:
        try:
            session.add(Billet(
                sale_id=billet_data.sale_id,
                value=billet_data.value,
                expire_date=billet_data.expire_date,
                status=billet_data.status,
                transaction_id=billet_data.transaction_id,
                barcode=billet_data.barcode,
                pixcode=billet_data.pixcode,
                billet_link=billet_data.billet_link,
                billet_pdf_link=billet_data.billet_pdf_link
            ))
            await session.commit()
            return Standard_Output(message='Operação efetuada com sucesso.')
        except IntegrityError:
            raise HTTPException(status_code=400, detail='Erro na requisição. Verifique os dados e tente novamente.')
        except DBAPIError as error:
            raise HTTPException(status_code=400, detail='Erro na requisição. Verifique os dados e tente novamente.')
        except Exception as error:
            await session.close()
            session.add(Error_Logs(
                str(error), datetime.now(), None, 1, 'service billet_register_'
            ))
            await session.commit()
            raise HTTPException(status_code=500, detail='Erro no servidor. Estamos trabalhando para corrigir')

async def billet_update_(billet_data):
    async with async_session() as session:
        try:
            result = await session.execute(
                select(Billet).where(Billet.id == billet_data.id)
            )
            # bdb = billet of database
            bdb = result.scalars().first()

            bdb.value = billet_data.value if billet_data.value else bdb.value
            bdb.expire_date = billet_data.expire_date if billet_data.expire_date else bdb.expire_date
            bdb.status = billet_data.status if billet_data.status else bdb.status
            bdb.transaction_id = billet_data.transaction_id if billet_data.transaction_id else bdb.transaction_id
            bdb.barcode = billet_data.barcode if billet_data.barcode else bdb.barcode
            bdb.pixcode = billet_data.pixcode if billet_data.pixcode else bdb.pixcode
            bdb.billet_link = billet_data.billet_link if billet_data.billet_link else bdb.billet_link
            bdb.billet_pdf_link = billet_data.billet_pdf_link if billet_data.billet_pdf_link else bdb.billet_pdf_link

            session.add(bdb)
            await session.commit()
            return Standard_Output(message='Operação efetuada com sucesso.')
        except AttributeError:
            raise HTTPException(status_code=400, detail='Identificador inválido. Revise os dados e tente novamente.')
        except IntegrityError:
            raise HTTPException(status_code=400, detail='Erro na requisição. Verifique os dados e tente novamente.')
        except DBAPIError:
            raise HTTPException(status_code=400, detail='Erro na requisição. Verifique os dados e tente novamente.')
        except Exception as error:
            await session.close()
            session.add(Error_Logs(
                str(error), datetime.now(), None, 1, 'service billet_update_'
            ))
            await session.commit()
            raise HTTPException(status_code=500, detail='Erro no servidor. Estamos trabalhando para corrigir')

async def get_billet_(type_data, billet_data):
    async with async_session() as session:
        try:
            if type_data == 'id':
                result = await session.execute(select(Billet).where(Billet.id == billet_data))
                billet_db = result.scalars().all()
            elif type_data == 'sale_id':
                result = await session.execute(select(Billet).where(Billet.sale_id == billet_data))
                billet_db = result.scalars().all()
            elif type_data == 'expire_date':
                result = await session.execute(select(Billet).where(Billet.expire_date == billet_data))
                billet_db = result.scalars().all()
            elif type_data == 'status':
                result = await session.execute(select(Billet).where(Billet.status == billet_data))
                billet_db = result.scalars().all()
            else:
                raise HTTPException(status_code=400, detail='O campo type_data está incorreto')

            for i, item in enumerate(billet_db):
                data = Billet_(
                    id=item.id,
                    sale_id=item.sale_id,
                    value=item.value,
                    expire_date=item.expire_date,
                    status=item.status,
                    transaction_id=item.transaction_id,
                    barcode=item.barcode,
                    pixcode=item.pixcode,
                    billet_link=item.billet_link,
                    billet_pdf_link=item.billet_pdf_link,
                )
                billet_db[i] = data
            return billet_db
        except HTTPException:
            raise HTTPException(status_code=400, detail='O campo type_data está incorreto')
        except IntegrityError:
            raise HTTPException(status_code=400, detail='Erro na requisição. Verifique os dados e tente novamente.')
        except DBAPIError:
            raise HTTPException(status_code=400, detail='Erro na requisição. Verifique os dados e tente novamente.')
        except Exception as error:
            await session.close()
            session.add(Error_Logs(
                str(error), datetime.now(), None, 1, 'service get_billet'
            ))
            await session.commit()
            raise HTTPException(status_code=500, detail='Erro no servidor. Estamos trabalhando para corrigir')