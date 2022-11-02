from datetime import datetime
from models.basemodels import Standard_Output
from models.connection import async_session
from models.tables import Access, Error_Logs
from sqlalchemy.exc import IntegrityError, DBAPIError
from fastapi import HTTPException


async def access_register_(access_data):
    async with async_session() as session:
        try:
            session.add(Access(
                user_id=access_data.user_id,
                access_datetime=access_data.access_datetime,
                endpoint=access_data.endpoint
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
                str(error), datetime.now(), None, 1, 'service access_register_'
            ))
            await session.commit()
            raise HTTPException(status_code=500, detail='Erro no servidor. Estamos trabalhando para corrigir')
