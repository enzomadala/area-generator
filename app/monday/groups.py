import requests
import json

MONDAY_API_URL = "https://api.monday.com/v2"


def create_group(board_id: int, group_name: str, token: str) -> str:
    query = """
    mutation ($board_id: ID!, $group_name: String!) {
        create_group(board_id: $board_id, group_name: $group_name) {
            id
        }
    }
    """

    variables = {
        "board_id": board_id,
        "group_name": group_name
    }

    response = requests.post(
        MONDAY_API_URL,
        json={"query": query, "variables": variables},
        headers={"Authorization": token}
    ).json()

    if "errors" in response:
        raise RuntimeError(response["errors"])

    return response["data"]["create_group"]["id"]