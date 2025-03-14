import requests

from services.general.helpers.base_helper import BaseHelper


class GradeHelper(BaseHelper):
    ENDPOINT_PREFIX = "/grade"
    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"

    def post_grade(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response