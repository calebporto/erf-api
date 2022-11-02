from fastapi import FastAPI, Request
from endpoints import access_endpoints, billet_endpoints, error_logs_endpoints, invoice_endpoints, item_endpoints, permission_endpoints, person_endpoints, sale_endpoints


app = FastAPI(
    title='Plataforma Bonsucesso - API',
    description='API destinada a transações com o banco de dados da aplicação.',
    version=1.0
)

@app.middleware('http')
async def auth(request: Request, call_next):
    '''
    Middleware para filtro de requisições.
    Verifica se a requisição contém os padrões exigidos.
    '''
    print('Antes')

    response = await call_next(request)

    print('Depois')
    return response

app.include_router(access_endpoints.router)
app.include_router(billet_endpoints.router)
app.include_router(error_logs_endpoints.router)
app.include_router(invoice_endpoints.router)
app.include_router(item_endpoints.router)
app.include_router(permission_endpoints.router)
app.include_router(person_endpoints.router)
app.include_router(sale_endpoints.router)