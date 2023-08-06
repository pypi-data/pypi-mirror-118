import requests

from cf_cli.backend.endpoints.core import BASE_URL, HEADERS

def verify(token: str):
    endpoint = f"{BASE_URL}/user/tokens/verify"
    HEADERS["Authorization"] = f"Bearer {token}"
    resp = requests.get(
        endpoint,
        headers=HEADERS
    ).json()
    print(resp)
    return resp['success']