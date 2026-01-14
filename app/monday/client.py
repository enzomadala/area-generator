import requests

MONDAY_API_URL = "https://api.monday.com/v2"

def monday_request(query: str, variables: dict, token: str):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    response = requests.post(
        MONDAY_API_URL,
        json={"query": query, "variables": variables},
        headers=headers
    )

    response.raise_for_status()
    data = response.json()

    if "errors" in data:
        raise RuntimeError(data["errors"])

    return data