from app.monday.client import monday_request


def create_group(board_id: int, group_name: str, token: str) -> str:
    query = """
    mutation ($board_id: ID!, $group_name: String!) {
      create_group(board_id: $board_id, group_name: $group_name) {
        id
      }
    }
    """
    res = monday_request(query, {"board_id": board_id, "group_name": group_name}, token)
    return res["data"]["create_group"]["id"]