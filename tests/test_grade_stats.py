import pytest
import requests
from faker import Faker

fake = Faker()


def test_get_grades_stats(access_token, headers, load_config):
    base_url = load_config["api_url"]
    response = requests.get(f"{base_url}/grades/stats", headers=headers)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response: {response.text}"


def test_get_grades_stats_not_authorized(access_token, fake_jwt, load_config):
    base_url = load_config["api_url"]
    response = requests.get(f"{base_url}/grades/stats", headers=fake_jwt)
    assert response.status_code == 403, f"Expected status code 403, but got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert "error" in data, "Response does not contain 'error' key"
    assert data["error"] == "Forbidden", "Expected 'error' message to be 'Forbidden'"


def test_get_grades_stats_forbidden(load_config):
    base_url = load_config["api_url"]
    response = requests.get(f"{base_url}/grades/stats")
    assert response.status_code == 403, f"Expected status code 403, but got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert "error" in data, "Response does not contain 'error' key"
    assert data["error"] == "Forbidden", "Expected 'error' message to be 'Forbidden'"


def test_get_grades_stats_validation_error(access_token, headers, load_config):
    base_url = load_config["api_url"]
    response = requests.get(f"{base_url}/grades/stats?student_id=not", headers=headers)  #  я передаю неверный тип данных и по идее должно работать
    assert response.status_code == 422, f"Expected status code 422, but got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert "error" in data, "Response does not contain 'error' key"
    assert data["error"] == "Validation Error", "Expected 'error' message to indicate Validation Error"


def test_create_grade(setup_class, access_token, headers, load_config):
    base_url = load_config["api_url"]

    payload_grades = {
        "teacher_id": fake.random_int(min=1, max=100),
        "student_id": fake.random_int(min=1, max=100),
        "grade": fake.random_int(min=1, max=5)
    }

    response = requests.post(f"{base_url}/grades/", headers=headers, json=payload_grades)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}. Response: {response.text}"


def test_get_grades(access_token, headers, load_config):
    base_url = load_config["api_url"]
    response = requests.get(f"{base_url}/grades/", headers=headers)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response: {response.text}"


@pytest.fixture(scope="function", autouse=False)
def setup_delete_group(access_token, headers, load_config):
    base_url = load_config["api_url"]
    payload_group = {
        "name": fake.word()

    }
    response = requests.post(f"{base_url}/groups/", headers=headers, json=payload_group)
    group_id = response.json().get("id")
    return group_id

def test_delete_group(setup_delete_group, access_token, headers, load_config):
    base_url = load_config["api_url"]
    group_id = setup_delete_group

    response = requests.delete(f"{base_url}/groups/{group_id}/", headers=headers)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response: {response.text}"
    response_check = requests.get(f"{base_url}/groups/{group_id}/", headers=headers)
    assert response_check.status_code == 404, f"Expected status code 404, but got {response_check.status_code}. Response: {response_check.text}"
