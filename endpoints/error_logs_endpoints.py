from fastapi import APIRouter

from models.basemodels import Error_Logs_, Standard_Output
from services.error_logs_service import add_error_log_

router = APIRouter(prefix='/error-logs-service')


@router.post('/add-error-log', response_model=Standard_Output)
async def add_error_log(log_data: Error_Logs_):
    '''
    Registra log de erros da aplicação
    :user_id se refere ao usuário que obteve o erro,
    caso esteja usando o front-end.
    :service_id se refere ao serviço que gerou o erro, sendo:
    1 - API
    2 - Front-end
    '''
    return await add_error_log_(log_data)