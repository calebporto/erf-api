from datetime import datetime
from models.connection import async_session
from models.tables import Error_Logs

async def add_error_log(log, endpoint):
    async with async_session() as session:
        try:
            session.add(Error_Logs(log, datetime.now(), None, 1, endpoint))
            await session.commit()
        except Exception as error:
            print(str(error))
            await session.close()
            await session.add(Error_Logs(str(error), datetime.now(), None, 1, 'service_add_error_log'))
