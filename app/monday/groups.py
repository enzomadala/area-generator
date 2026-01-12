from app.monday.client import monday_request

def create_group(board_id: int, group_name: str, token: str) -> str:
    query = """
    mutation ($board: Int!, $title: String!) {
      create_group (board_id: $board, group_name: $title) {
        id
      }
    }
    """

    variables = {
        "board": board_id,
        "title": group_name
    }

    data = monday_request(query, variables, token)
    return data["data"]["create_group"]["id"]