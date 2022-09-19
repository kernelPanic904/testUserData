from asyncio import run as asyncio_run

from uvicorn import Config, Server

from app.core.config import settings


async def start_app() -> None:
    config = Config(
        'app.main:app',
        host=settings.APP_HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL,
        reload=settings.RELOAD,
    )
    server = Server(config=config)
    await server.serve()


if __name__ == '__main__':
    asyncio_run(start_app())
