from models.basemodels import Standard_Output, Invoice_
from sqlalchemy.exc import DBAPIError, IntegrityError
from models.tables import Invoice, Error_Logs
from models.connection import async_session
from sqlalchemy.future import select
from fastapi import HTTPException
from datetime import datetime

async def invoice_register_(invoice_data):
    async with async_session() as session:
        try:
            session.add(Invoice(
                sale_id=invoice_data.sale_id,
                value=invoice_data.value,
                invoice_datetime=invoice_data.invoice_datetime,
                uuid=invoice_data.uuid,
                status=invoice_data.status,
                nfe_number=invoice_data.nfe_number,
                receipt=invoice_data.receipt,
                access_key=invoice_data.access_key,
                xml=invoice_data.xml,
                danfe=invoice_data.danfe
            ))
            await session.commit()
            return Standard_Output(message='Operação efetuada com sucesso.')
        except IntegrityError:
            raise HTTPException(status_code=400, detail='Erro na requisição. Verifique os dados.')
        except DBAPIError:
            raise HTTPException(status_code=400, detail='Erro na requisição. Verifique os dados.')
        except Exception as error:
            await session.close()
            session.add(Error_Logs(
                str(error), datetime.now(), None, 1, 'service invoice_register_'
            ))
            await session.commit()
            raise HTTPException(status_code=500, detail='Erro no servidor. Estamos trabalhando para corrigir')

async def invoice_update_(invoice_data):
    async with async_session() as session:
        try:
            result = await session.execute(
                select(Invoice).where(Invoice.id == invoice_data.id)
            )
            invoice_db = result.scalars().first()

            idt, idb = invoice_data, invoice_db

            idb.value = idt.value if idt.value else idb.value
            idb.invoice_datetime = idt.invoice_datetime if idt.invoice_datetime else idb.invoice_datetime
            idb.uuid = idt.uuid if idt.uuid else idb.uuid
            idb.status = idt.status if idt.status else idb.status
            idb.nfe_number = idt.nfe_number if idt.nfe_number else idb.nfe_number
            idb.receipt = idt.receipt if idt.receipt else idb.receipt
            idb.access_key = idt.access_key if idt.access_key else idb.access_key
            idb.xml = idt.xml if idt.xml else idb.xml
            idb.danfe = idt.danfe if idt.danfe else idb.danfe

            session.add(idb)
            await session.commit()
            return Standard_Output(message='Identificador inválido. Verifique os dados.')
        except AttributeError:
            raise HTTPException(status_code=400, detail='Erro na requisição. Verifique os dados.')
        except IntegrityError:
            raise HTTPException(status_code=400, detail='Erro na requisição. Verifique os dados.')
        except DBAPIError:
            raise HTTPException(status_code=400, detail='Erro na requisição. Verifique os dados.')
        except Exception as error:
            await session.close()
            session.add(Error_Logs(
                str(error), datetime.now(), None, 1, 'service invoice_update_'
            ))
            await session.commit()
            raise HTTPException(status_code=500, detail='Erro no servidor. Estamos trabalhando para corrigir')

async def get_invoice_(type_data, data):
    async with async_session() as session:
        try:
            if type_data == 'id':
                result = await session.execute(select(Invoice).where(Invoice.id == data))
                invoice_db = result.scalars().all()
            elif type_data == 'sale_id':
                result = await session.execute(select(Invoice).where(Invoice.sale_id == data))
                invoice_db = result.scalars().all()
            elif type_data == 'invoice_datetime':
                result = await session.execute(select(Invoice).where(Invoice.invoice_datetime == data))
                invoice_db = result.scalars().all()
            elif type_data == 'status':
                result = await session.execute(select(Invoice).where(Invoice.status == data))
                invoice_db = result.scalars().all()
            else:
                raise HTTPException(status_code=400, detail='O campo type_data não corresponde a um campo válido.')

            for i, item in enumerate(invoice_db):
                data = Invoice_(
                    id=item.id,
                    sale_id=item.sale_id,
                    value=item.value,
                    invoice_datetime=item.invoice_datetime,
                    uuid=item.uuid,
                    status=item.status,
                    nfe_number=item.nfe_number,
                    receipt=item.receipt,
                    access_key=item.access_key,
                    xml=item.xml,
                    danfe=item.danfe
                )
                invoice_db[i] = data
            return invoice_db
        except HTTPException as error:
            raise HTTPException(status_code=error.status_code, detail=error.detail)
        except IntegrityError:
            raise HTTPException(status_code=400, detail='Erro na requisição. Verifique os dados.')
        except DBAPIError:
            raise HTTPException(status_code=400, detail='Erro na requisição. Verifique os dados.')
        except Exception as error:
            await session.close()
            session.add(Error_Logs(
                str(error), datetime.now(), None, 1, 'service get_invoice_'
            ))
            await session.commit()
            raise HTTPException(status_code=500, detail='Erro no servidor. Estamos trabalhando para corrigir')