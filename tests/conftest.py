import time

import pytest
import requests
from faker import Faker

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
def setup(access_token):

    ENDPOINT = "http://127.0.0.1:8001"

    fake = Faker()
    yield {
        "endpoint": ENDPOINT,
        "fake": fake,
        "access_token": access_token
    }



