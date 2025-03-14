import pytest
import requests

ENDPOINT = "http://127.0.0.1:8001"


def test_get_grades_stats(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(ENDPOINT + "/grades/stats", headers=headers)
    assert response.status_code == 200


def test_get_grades_stats_student(access_token): # почему в этом тесте ошибка 422, валидация?
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(ENDPOINT + "/grades/stats?student_id", headers=headers) # с квери параметром
    assert response.status_code == 200


def test_create_grade(access_token): # и в этом ошибка с валидацией
    payload = {
        "teacher_id": 1,
        "student_id": 1,
        "grade": 3
    }
    headers = {
        "Authorization": f"Bearer {access_token}"

    }

    response = requests.post(ENDPOINT + "/grades/", headers=headers, json=payload)
    assert response.status_code == 201


def test_get_grade(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(ENDPOINT + "/grades", headers=headers)
    assert response.status_code == 200
