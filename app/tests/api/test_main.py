from json import dumps
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient

from app.db.base_class import Base
from app.api.deps import get_db
from app.main import app
from app.core.config import settings

api_path = settings.API_STR + settings.API_V1_STR

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app=app)

TEST_HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}
TEST_USERS = [
    {
        "phone_number": "78523147026",
        "name": "Иван",
        "surname": "Петров",
        "patronymic": "Васильевич",
        "email": "ivan454@example.com",
        "country": "Россия"
    },
    {
        "phone_number": "78523147025",
        "name": "Петр",
        "surname": "Иванов",
        "patronymic": "Иванович",
        "email": "petr545@example.com",
        "country": "Таджикистан"
    },
    {
        "phone_number": "78523147024",
        "name": "Саша",
        "surname": "Петров",
        "patronymic": "Петрович",
        "email": "sasha455@example.com",
        "country": "РФ"
    },
]


def test_does_not_exist():
    response = client.post(
        url=api_path + '/users/get',
        data=dumps({'phone_number': '79827322127'}),
        headers=TEST_HEADERS,
    )
    assert response.status_code == 404


def test_create_user_data():
    for user_data in TEST_USERS:
        response = client.post(
            url=api_path + '/users/create',
            data=dumps(user_data),
            headers=TEST_HEADERS,
        )
        assert response.status_code == 201
        assert response.json()['phone_number'] == user_data['phone_number']


def test_delete_user_data():
    user_data = TEST_USERS[0]
    response = client.post(
        url=api_path + '/users/create',
        data=dumps(user_data),
        headers=TEST_HEADERS,
    )
    assert response.status_code == 201
    created_user_phone = response.json()['phone_number']
    response = client.post(
        url=api_path + '/users/remove',
        data=dumps({'phone_number': created_user_phone})
    )
    assert response.status_code == 201
