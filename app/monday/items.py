from app.monday.client import monday_request


def create_item(board_id: int, group_id: str, item_name: str, token: str):
    query = """
    mutation ($board_id: ID!, $group_id: String!, $item_name: String!) {
      create_item(board_id: $board_id, group_id: $group_id, item_name: $item_name) {
        id
      }
    }
    """
    monday_request(
        query,
        {"board_id": board_id, "group_id": group_id, "item_name": item_name},
        token
    )