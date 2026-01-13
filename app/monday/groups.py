import requests
import json
from app.monday.client import monday_request

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

def get_default_group(board_id: int, token: str) -> str:
    query = """
    query ($board_id: [ID!]) {
      boards(ids: $board_id) {
        groups {
          id
          title
        }
      }
    }
    """

    variables = {"board_id": board_id}

    response = monday_request(query, variables, token)

    # 🔥 PROTEÇÃO OBRIGATÓRIA
    if "errors" in response:
        raise RuntimeError(
            f"Erro ao buscar grupos do board {board_id}: {response['errors']}"
        )

    boards = response.get("data", {}).get("boards", [])

    if not boards or not boards[0]["groups"]:
        raise RuntimeError(
            f"Board {board_id} não retornou grupos (ainda não pronto?)"
        )

    # Monday sempre cria um grupo default
    return boards[0]["groups"][0]["id"]