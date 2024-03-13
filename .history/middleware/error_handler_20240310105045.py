'''
Esta archivo maneja los errores que se producen a nivel de sistema
Genera un codi HTTP 500 como error
created 2023-12
'''
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
# esto se incorporo para la sintaxis nueva de python
from typing import Union
import os
import logging

# Verificar si la carpeta 'api_logs' existe, si no, crearla
if not os.path.exists('api_logs'):
    os.makedirs('api_logs')

# Configurar el logging para escribir en el archivo 'errores.log' dentro de 'api_logs'
logging.basicConfig(filename='api_logs/errores.log', encoding='utf-8', level=logging.DEBUG)

# Escribir un mensaje de error en el archivo
logging.error('Este es un mensaje de error')


class ErrorHandler(BaseHTTPMiddleware):
    #constructor
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
    
    #este método es el que se ejecuta cuando ocurre un error
    async def dispatch(self, request: Request, call_next) -> Union[Response, JSONResponse]:    
        try:
            return await call_next(request)
        except Exception as e:
            return JSONResponse(status_code=500,content={'message':str(e)})
