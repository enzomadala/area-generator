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

    response = monday_request(query, variables, token)

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

    variables = {
        "board_id": board_id
    }

    response = monday_request(query, variables, token)

    if "errors" in response:
        raise RuntimeError(response["errors"])

    return response["data"]["boards"][0]["groups"][0]["id"]