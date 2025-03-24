import time
import jwt
from datetime import datetime, timedelta
import secrets
import pytest
import requests

from faker import Faker

from configs.Config_Reader import config
from services.auth.auth_service import AuthService
from services.auth.models.login_request import LoginRequest
from services.auth.models.register_request import RegisterRequest
from services.university.university_service import UniversityService
from utils.api_utils import ApiUtils

faker = Faker()


@pytest.fixture(scope="session", autouse=True)
def auth_service_readiness():
    timeout = 180
    start_time = time.time()
    while time.time() < start_time + timeout:
        try:
            response = requests.get(AuthService.SERVICE_URL + "/docs")
            response.raise_for_status()
        except:
            time.sleep(1)  # try again in 1 second
        else:
            break
    else:
        raise RuntimeError(f"Auth service wasn't started during '{timeout}' seconds.")


@pytest.fixture(scope="session", autouse=True)
def university_service_readiness():
    timeout = 180
    start_time = time.time()
    while time.time() < start_time + timeout:
        try:
            response = requests.get(UniversityService.SERVICE_URL + "/docs")
            response.raise_for_status()
        except requests.exceptions.Timeout as e:
            print("Request timed out:", e)
            time.sleep(1)
        else:
            break
    else:
        raise RuntimeError(f"University service wasn't started during '{timeout}' seconds.")


@pytest.fixture(scope="function", autouse=False)
def auth_api_utils_anonym():
    api_utils = ApiUtils(url=AuthService.SERVICE_URL)
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def university_api_utils_anonym():
    api_utils = ApiUtils(url=UniversityService.SERVICE_URL)
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def access_token(auth_api_utils_anonym):
    auth_service = AuthService(auth_api_utils_anonym)
    username = faker.user_name()
    password = faker.password(length=30,
                              special_chars=True,
                              digits=True,
                              upper_case=True,
                              lower_case=True)
    auth_service.register_user(
        register_request=RegisterRequest(
            username=username,
            password=password,
            password_repeat=password,
            email=faker.email()))
    login_response = auth_service.login_user(LoginRequest(username=username, password=password))
    return login_response.access_token


@pytest.fixture(scope="function", autouse=False)
def auth_api_utils_admin(access_token):
    api_utils = ApiUtils(url=AuthService.SERVICE_URL, headers={"Authorization": f"Bearer {access_token}"})
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def university_api_utils_admin(access_token):
    api_utils = ApiUtils(url=UniversityService.SERVICE_URL, headers={"Authorization": f"Bearer {access_token}"})
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def headers(access_token):
    return {
        "Authorization": f"Bearer {access_token}"
    }


@pytest.fixture(scope="function", autouse=False)
def fake_jwt():
    key = "secret"
    encoded = jwt.encode({"some": "payload"}, key, algorithm="HS256")
    decoded = jwt.decode(encoded, key, algorithms=["HS256"])

    return {
        "Authorization": f"Bearer {encoded}"
    }


@pytest.fixture
def load_config():
    return config()


@pytest.fixture(scope="function", autouse=False)
def group(headers):
    api_utils = ApiUtils(url=UniversityService.SERVICE_URL)
    payload_group = {
        "name": faker.word()
    }
    response = requests.post(api_utils.url + "/groups/", headers=headers, json=payload_group)
    group_id = response.json().get("id")

    yield group_id

    if group_id:
        requests.delete(api_utils.url + f"/groups/{group_id}/", headers=headers)


@pytest.fixture(scope="function", autouse=False)
def student(headers):
    api_utils = ApiUtils(url=UniversityService.SERVICE_URL)
    payload_student = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.email(),
        "degree": faker.random_element(elements=("Bachelor", "Master")),
        "phone": faker.numerify("+7##########"),
        "group_id": 1
    }
    response_student = requests.post(api_utils.url + "/students/", headers=headers, json=payload_student)
    student_id = response_student.json().get("id")
    yield student_id


@pytest.fixture(scope="function", autouse=False)
def teacher(headers):
    api_utils = ApiUtils(url=UniversityService.SERVICE_URL)
    payload_teacher = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "subject": faker.random_element(elements=("Geography", "History"))
    }
    response_teacher = requests.post(api_utils.url + "/teachers/", headers=headers, json=payload_teacher)
    teacher_id = response_teacher.json().get("id")
    yield teacher_id
