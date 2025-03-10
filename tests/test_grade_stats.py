import pytest
import requests

from logger.logger import Logger
from utils.api_utils import ApiUtils
from faker import Faker
from services.university.university_service import UniversityService
from university.models.base_grade import BaseGrade

faker = Faker()


class TestStatisticsAPI:

    def test_statistics(self, ids, university_api_utils_admin):
        endpoint = ApiUtils(url=UniversityService.SERVICE_URL)
        api_key = ids(api_utils=university_api_utils_admin)
        Logger.info("### Steps 1. Create ids")
        params = {
            "student_id": ids["student_id"],
            "teacher_id": ids["teacher_id"],
            "group_id": ids["group_id"]
        }

        response = requests.get(endpoint, params=params)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

        response_json = api_key.create_grades(grade_request=ids)
        assert response_json.BaseGrade == ids.id, \
            f"Wrong group id. Actual: '{response_json.group_id}', but expected: '{ids.id}'"
