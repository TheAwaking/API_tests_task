import pytest
import requests
from faker import Faker


# ENDPOINT = "http://127.0.0.1:8001"


def test_get_grades_stats(access_token, headers, setup):
    response = requests.get(setup['endpoint'] + "/grades/stats", headers=headers)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response: {response.text}"


def test_get_grades_stats_not_authorized(access_token, headers, setup):
    response = requests.get(setup['endpoint'] + "/grades/stats", headers=headers)
    assert response.status_code == 401, f"Expected status code 401, but got {response.status_code}. Response: {response.text}"


def test_get_grades_stats_forbidden(setup):
    response = requests.get(setup['endpoint'] + "/grades/stats")
    assert response.status_code == 403, f"Expected status code 403, but got {response.status_code}. Response: {response.text}"


def test_get_grades_stats_validation_error(access_token, headers, setup):
    response = requests.get(setup['endpoint'] + "/grades/stats", headers=headers)
    assert response.status_code == 422, f"Expected status code 422, but got {response.status_code}. Response: {response.text}"


def test_create_student(access_token, headers, setup):
    payload_student = {
        "first_name": setup['fake'].first_name(),
        "last_name": setup['fake'].last_name(),
        "email": setup['fake'].email(),
        "degree": setup['fake'].random_element(elements=("Bachelor", "Master")),
        "phone": setup['fake'].numerify("+7##########"),
        "group_id": 1
    }
    response = requests.post(setup['endpoint'] + "/students/", headers=headers, json=payload_student)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}. Response: {response.text}"

    payload_group = {
        "name": setup['fake'].word()

    }
    response = requests.post(setup['endpoint'] + "/groups/", headers=headers, json=payload_group)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}. Response: {response.text}"

    payload_teacher = {

        "first_name": "First name",
        "last_name": "Last name",
        "subject": "Geography"

    }
    response = requests.post(setup['endpoint'] + "/teachers/", headers=headers, json=payload_teacher)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}. Response: {response.text}"

    payload_grades = {
        "teacher_id": 1,
        "student_id": 1,
        "grade": 3,
    }

    response = requests.post(setup['endpoint'] + "/grades/", headers=headers, data=payload_grades)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}. Response: {response.text}"


def test_get_grades(access_token, headers, setup):
    response = requests.get(setup['endpoint'] + "/grades/", headers=headers)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response: {response.text}"


def test_delete_group(access_token, headers, setup):
    payload_group = {
        "name": setup['fake'].word()

    }
    response = requests.post(setup['endpoint'] + "/groups/", headers=headers, json=payload_group)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}. Response: {response.text}"

    group_id = response.json().get("id")

    response = requests.delete(setup['endpoint'] + f"/groups/{group_id}/", headers=headers)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response: {response.text}"
