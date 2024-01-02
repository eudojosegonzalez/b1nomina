from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
# esto se incorporo para la sintaxis nueva de python
from typing import Union

class ErrorHandler(BaseHTTPMiddleware):
    #constructor
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
    
    #este método es el que se ejcuta cuando ocurre un error
    # sintaxis vieja
    #async def dispacth(self, request: Request, call_next) -> Response | JSONResponse:
    # sintaxis nueva
    async def dispatch(self, request: Request, call_next) -> Union[Response, JSONResponse]:    
        try:
            return await call_next(request)
        except Exception as e:
            return JSONResponse(status_code=500,content={'message':str(e)})
