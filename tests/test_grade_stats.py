import pytest
import requests

from logger.logger import Logger
from services.university.helpers.grade_helper import GradeHelper
from utils.api_utils import ApiUtils
from services.university.university_service import UniversityService


class TestStatisticsAPI:
    ENDPOINT = "http://127.0.0.1:8001"

    def test_can_create_task():
        payload = {
            "count": 3,
            "min": 2,
            "max": 5,
            "avg": 3.75
        }
        response = requests.get(ENDPOINT + "/grades/stats", json=payload)
        assert response.status_code == 200

        data = response.json()
        student_id = data["student_id"]
        teacher_id = data["teacher_id"]
        group_id = data["group_id"]
        get_response = requests.get(ENDPOINT + "/grades/stats")

        assert get_response.status_code == 200
        get_grades_data = get_response.json()
        assert get_grades_data["count"] == payload["count"]
        assert get_grades_data["min"] == payload["min"]
        assert get_grades_data["max"] == payload["max"]
        assert get_grades_data["avg"] == payload["avg"]
