import requests

MONDAY_API_URL = "https://api.monday.com/v2"


def monday_request(query: str, variables: dict | None = None, token: str | None = None):
    if not token:
        raise Exception("Token não informado")

    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    response = requests.post(MONDAY_API_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()