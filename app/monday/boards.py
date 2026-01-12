import requests
from app.monday.groups import create_group
from app.monday.items import create_lote_item

MONDAY_API_URL = "https://api.monday.com/v2"


def duplicate_board(template_id: int, name: str, token: str) -> int:
    query = f"""
    mutation {{
      duplicate_board(
        board_id: {template_id},
        board_name: "{name}",
        duplicate_type: duplicate_board_with_structure
      ) {{
        board {{
          id
        }}
      }}
    }}
    """

    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    response = requests.post(
        MONDAY_API_URL,
        json={"query": query},
        headers=headers
    )

    data = response.json()
    print("📡 RESPOSTA DUPLICATE_BOARD:", data)

    if "errors" in data:
        raise Exception(f"Erro ao duplicar board: {data['errors']}")

    return int(data["data"]["duplicate_board"]["board"]["id"])


def populate_board_with_lotes(board_id: int, agrupamentos: dict, token: str):
    for group_name, data in agrupamentos.items():
        group_id = create_group(board_id, group_name, token)

        for lote in data["lotes"]:
            create_lote_item(
                board_id=board_id,
                group_id=group_id,
                lote=lote,
                token=token
            )