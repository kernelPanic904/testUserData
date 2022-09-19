from os import environ

from pydantic import BaseConfig


class Settings(BaseConfig):
    API_V1_STR: str = '/api_v1'
    API_STR: str = '/api'
    APP_HOST: str = '0.0.0.0'
    PORT: int = 8000
    RELOAD: bool = True
    LOG_LEVEL: str = 'info'

    DB_USERNAME: str = environ.get('POSTGRES_USER', 'postgres')
    DB_PASSWORD: str = environ.get('POSTGRES_PASSWORD', '1')
    DB_DRIVER: str = environ.get('POSTGRES_DRIVER', 'postgresql')
    DB_NAME: str = environ.get('POSTGRES_DB', 'user_data_db')
    DB_HOST: str = environ.get('POSTGRES_HOST', 'localhost')
    DB_PORT: str = environ.get('POSTGRES_PORT', '5432')

    REDIS_HOST: str = environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT: str = environ.get('REDIS_PORT', '6370')
    REDIS_DRIVER: str = environ.get('REDIS_DRIVER', 'redis')

    DB_URL: str = '{db_driver}://{db_user}:' \
                  '{db_password}@{db_host}:{db_port}/{db_name}'.format(
                        db_driver=DB_DRIVER,
                        db_user=DB_USERNAME,
                        db_password=DB_PASSWORD,
                        db_host=DB_HOST,
                        db_port=str(DB_PORT),
                        db_name=DB_NAME,
                    )
    REDIS_URL: str = '{redis_driver}://{redis_host}:{redis_port}'.format(
        redis_host=REDIS_HOST,
        redis_port=str(REDIS_PORT),
        redis_driver=REDIS_DRIVER,
    )
    DADATA_API_KEY: str = 'ddff5b52f50da87e4a5d1cc3074237bf531458c0'
    DADATA_COUNTRY_URL: str = 'https://suggestions.dadata.ru/' \
                              'suggestions/api/4_1/rs/suggest/country'


settings = Settings()
