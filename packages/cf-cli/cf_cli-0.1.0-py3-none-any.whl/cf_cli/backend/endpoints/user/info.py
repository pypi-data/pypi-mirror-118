import requests

from cf_cli.backend.endpoints.core import BASE_URL, HEADERS
from cf_cli.backend.schemas import User


def get_user_info():
    endpoint = f"{BASE_URL}/user"
    resp = requests.get(
        endpoint,
        headers=HEADERS
    ).json()
    if resp["success"]:
        resp["result"]["id_"] = resp["result"]["id"]
        del resp["result"]["id"]
        user: User = User.parse_obj(resp["result"])
        return user
    else:
        return False
