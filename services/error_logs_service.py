from datetime import datetime
from models.connection import async_session
from models.tables import Error_Logs
from fastapi import HTTPException
from models.basemodels import Standard_Output
from sqlalchemy.exc import IntegrityError, DBAPIError

async def add_error_log_(error_data):
    async with async_session() as session:
        try:
            session.add(Error_Logs(
                error_data.log,
                error_data.log_datetime,
                error_data.user_id,
                error_data.service_id,
                error_data.endpoint)
            )
            await session.commit()
            return Standard_Output(message='Operação efetuada com sucesso.')
        except IntegrityError:
            raise HTTPException(status_code=400, detail='Erro na requisição. Verifique os dados.')
        except DBAPIError:
            raise HTTPException(status_code=400, detail='Erro na requisição. Verifique os dados.')
        except Exception as error:
            await session.close()
            session.add(Error_Logs(
                str(error), datetime.now(), None, 1, 'service add_error_log_'))
            await session.commit()
            raise HTTPException(status_code=500, detail='Erro no servidor. Estamos trabalhando para corrigir')