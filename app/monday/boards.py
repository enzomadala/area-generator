import requests

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


def populate_board_with_lotes(board_id: int, lotes: list[int], token: str):
    query = """
    mutation ($board_id: ID!, $name: String!) {
      create_item(board_id: $board_id, item_name: $name) {
        id
      }
    }
    """

    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    for lote in lotes:
        response = requests.post(
            MONDAY_API_URL,
            json={
                "query": query,
                "variables": {
                    "board_id": board_id,
                    "name": str(lote)
                }
            },
            headers=headers
        )

        data = response.json()

        if "errors" in data:
            raise Exception(f"Erro ao criar lote {lote}: {data['errors']}")