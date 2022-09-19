from typing import Callable
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

from app.api.endpoints import api_router
from app.logger import logger

app = FastAPI()
app.include_router(api_router)


@app.middleware('http')
async def logging_requests(
        request: Request,
        call_next: Callable
) -> StreamingResponse:
    logger.info(request.url.path)
    logger.info(request.headers.items())

    time_start = datetime.utcnow()
    response: StreamingResponse = await call_next(request)
    time_delta = datetime.utcnow() - time_start

    logger.info(f'Request done for {time_delta}')
    logger.info(response.status_code)
    logger.info(response.headers)
    logger.info(response.body_iterator)
    return response
