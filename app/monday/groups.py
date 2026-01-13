import requests
import json


def create_group(board_id: int, group_name: str, token: str) -> str | None:
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
        "https://api.monday.com/v2",
        json={"query": query, "variables": variables},
        headers={
            "Authorization": token,
            "Content-Type": "application/json"
        }
    )
 
    data = response.json()

    # 🔹 Tratamento seguro (importantíssimo)
    if "errors" in data:
        print("❌ Erro ao criar group:", data["errors"])
        return None

    return data["data"]["create_group"]["id"]