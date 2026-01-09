import json
import requests

MONDAY_API_URL = "https://api.monday.com/v2"

def set_status(board_id: int, item_id: int, label: str, token: str):
    mutation = """
    mutation ($board: ID!, $item: ID!, $value: String!) {
      change_simple_column_value(
        board_id: $board,
        item_id: $item,
        column_id: "color_mkzdtnz7",
        value: $value
      ) {
        id
      }
    }
    """

    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    payload = {
        "query": mutation,
        "variables": {
            "board": board_id,
            "item": item_id,
            "value": label
        }
    }

    r = requests.post(MONDAY_API_URL, json=payload, headers=headers)
    data = r.json()

    if "errors" in data:
        raise Exception(data["errors"])