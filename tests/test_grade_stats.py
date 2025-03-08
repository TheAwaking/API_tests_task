import pytest
import requests
from utils.api_utils import ApiUtils
from faker import Faker
from services.university.university_service import UniversityService

faker = Faker()


class TestStatisticsAPI:

    def test_statistics(self, ids, university_api_utils_admin):
        endpoint = ApiUtils(url=UniversityService.SERVICE_URL)
        api_key = UniversityService(api_utils=university_api_utils_admin)
        params = {
            "student_id": ids["student_id"],
            "teacher_id": ids["teacher_id"],
            "group_id": ids["group_id"]
        }

        response = requests.get(endpoint, params=params)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

        response_json = response.json()
        assert response_json["count"] == 3, "'count' should be 3"
        assert response_json["min"] == 2, "'min' should be 2"
        assert response_json["max"] == 5, "'max' should be 5"
        assert response_json["avg"] == 3.75, "'avg' should be 3.75"
