import json
import requests

MONDAY_API_URL = "https://api.monday.com/v2"

def update_link_column(
    board_id: int,
    item_id: int,
    column_id: str,
    url: str,
    text: str,
    token: str
):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    value = json.dumps({
        "url": url,
        "text": text
    })

    query = """
    mutation ($board_id: ID!, $item_id: ID!, $column_id: String!, $value: JSON!) {
      change_column_value(
        board_id: $board_id,
        item_id: $item_id,
        column_id: $column_id,
        value: $value
      ) {
        id
      }
    }
    """

    variables = {
        "board_id": board_id,
        "item_id": item_id,
        "column_id": column_id,
        "value": value
    }

    response = requests.post(
        MONDAY_API_URL,
        json={"query": query, "variables": variables},
        headers=headers
    )

    data = response.json()

    if "errors" in data:
        raise Exception(data["errors"])