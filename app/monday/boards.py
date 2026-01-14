from app.monday.client import monday_request
from app.monday.groups import create_group
from app.monday.items import create_item


def duplicate_board(template_id: int, name: str, token: str) -> int:
    query = """
    mutation ($board_id: ID!, $name: String!) {
      duplicate_board(
        board_id: $board_id,
        duplicate_type: duplicate_board_with_structure,
        board_name: $name
      ) {
        board { id }
      }
    }
    """
    res = monday_request(query, {"board_id": template_id, "name": name}, token)
    return int(res["data"]["duplicate_board"]["board"]["id"])


def populate_board_with_lotes(board_id: int, agrupamentos: dict, token: str):
    for group, info in agrupamentos.items():
        group_id = create_group(board_id, group, token)
        for lote in info["lotes"]:
            create_item(board_id, group_id, f"Lote {lote}", token)