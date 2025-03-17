import pytest
import requests
from faker import Faker

fake = Faker()


def test_get_grades_stats(access_token, headers, load_config):
    base_url = load_config["api_url"]
    response = requests.get(f"{base_url}/grades/stats", headers=headers)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response: {response.text}"


def test_get_grades_stats_not_authorized(access_token, invalid_headers, load_config):
    base_url = load_config["api_url"]
    response = requests.get(f"{base_url}/grades/stats", headers=invalid_headers)
    assert response.status_code == 401, f"Expected status code 401, but got {response.status_code}. Response: {response.text}"


def test_get_grades_stats_forbidden(load_config):
    base_url = load_config["api_url"]

    response = requests.get(f"{base_url}/grades/stats")
    assert response.status_code == 403, f"Expected status code 403, but got {response.status_code}. Response: {response.text}"


def test_get_grades_stats_validation_error(access_token, headers, load_config):  #  тут я не могу вспомнить какой кейс применял,чтобы возращалась 422 от сервера
    base_url = load_config["api_url"]

    response = requests.get(f"{base_url}/grades/stats", headers=headers)
    assert response.status_code == 422, f"Expected status code 422, but got {response.status_code}. Response: {response.text}"


def test_create_grade(setup, access_token, headers, load_config):
    base_url = load_config["api_url"]


    payload_grades = {
        "teacher_id": 1,
        "student_id": 1,
        "grade": 3,
    }


    response = requests.post(f"{base_url}/grades/", headers=headers, json=payload_grades)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}. Response: {response.text}"


def test_get_grades(access_token, headers, load_config):
    base_url = load_config["api_url"]
    response = requests.get(f"{base_url}/grades/", headers=headers)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response: {response.text}"


def test_delete_group(setup_delete, access_token, headers, load_config):
    base_url = load_config["api_url"]
    group_id = setup_delete

    response = requests.delete(f"{base_url}/groups/{group_id}/", headers=headers)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response: {response.text}"
