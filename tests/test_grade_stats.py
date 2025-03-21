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
    assert response.status_code == 401, f"Expected status code 401, but got {response.status_code}. Response: {response.text}"


def test_get_grades_stats_authorization_error_message(access_token, fake_jwt, load_config):
    base_url = load_config["api_url"]
    response = requests.get(f"{base_url}/grades/stats", headers=fake_jwt)
    assert response.status_code == 401, f"Expected status code 401, but got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert "error" in data, "Response does not contain 'error' key"
    assert data["error"] == "Not authorized", "Expected 'error' message to be 'Not authorized'"


def test_get_grades_stats_forbidden(access_token, load_config):
    base_url = load_config["api_url"]
    response = requests.get(f"{base_url}/grades/stats")
    assert response.status_code == 403, f"Expected status code 403, but got {response.status_code}. Response: {response.text}"


def test_get_grades_stats_forbidden_error_message(access_token, load_config):
    base_url = load_config["api_url"]
    response = requests.get(f"{base_url}/grades/stats")
    assert response.status_code == 403, f"Expected status code 403, but got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert "error" in data, "Response does not contain 'error' key"
    assert data["error"] == "Forbidden", "Expected 'error' message to be 'Forbidden'"


def test_get_grades_stats_validation_error(access_token, headers, load_config):
    base_url = load_config["api_url"]
    payload = {'student_id': 'not'}
    response = requests.get(f"{base_url}/grades/stats", params=payload, headers=headers)
    assert response.status_code == 422, f"Expected status code 422, but got {response.status_code}. Response: {response.text}"


def test_get_grades_stats_validation_error_message(access_token, headers, load_config):
    base_url = load_config["api_url"]
    payload = {'student_id': 'not'}
    response = requests.get(f"{base_url}/grades/stats", params=payload, headers=headers)
    assert response.status_code == 422, f"Expected status code 422, but got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert "error" in data, "Response does not contain 'error' key"
    assert data["error"] == "Validation Error", "Expected 'error' message to indicate Validation Error"


def test_create_grade(setup_class, access_token, headers, load_config):
    base_url = load_config["api_url"]
    student_id = setup_class["student_id"]
    teacher_id = setup_class["teacher_id"]

    payload_grades = {
        "teacher_id": teacher_id,
        "student_id": student_id,
        "grade": fake.random_int(min=0, max=5)
    }

    response = requests.post(f"{base_url}/grades/", headers=headers, json=payload_grades)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}. Response: {response.text}"


def test_get_grades(access_token, headers, load_config):
    base_url = load_config["api_url"]
    response = requests.get(f"{base_url}/grades/", headers=headers)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response: {response.text}"


def test_delete_group(group, access_token, headers, load_config):
    base_url = load_config["api_url"]
    group_id = group

    response = requests.delete(f"{base_url}/groups/{group_id}/", headers=headers)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response: {response.text}"


def test_delete_group_verification_after_delete(group, access_token, headers, load_config):
    base_url = load_config["api_url"]
    group_id = group

    response = requests.delete(f"{base_url}/groups/{group_id}/", headers=headers)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response: {response.text}"
    response_check = requests.get(f"{base_url}/groups/{group_id}/", headers=headers)
    assert response_check.status_code == 404, f"Expected status code 404, but got {response_check.status_code}. Response: {response_check.text}"
