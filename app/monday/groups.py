import requests
from app.monday.groups import create_group
from app.monday.items import create_lote_item

MONDAY_API_URL = "https://api.monday.com/v2"


def create_group(board_id: int, group_name: str, token: str) -> str:
    query = """
    mutation ($board_id: ID!, $group_name: String!) {
      create_group (board_id: $board_id, group_name: $group_name) {
        id
      }
    }
    """

    response = requests.post(
        MONDAY_API_URL,
        json={
            "query": query,
            "variables": {
                "board_id": board_id,
                "group_name": group_name
            }
        },
        headers={
            "Authorization": token,
            "Content-Type": "application/json"
        }
    )

    data = response.json()

    # 🔴 ERRO DO MONDAY
    if "errors" in data:
        print("❌ ERRO AO CRIAR GROUP NO MONDAY")
        print("📛 Group:", group_name)
        print("📦 Resposta:", data)
        raise RuntimeError(
            f"Erro ao criar grupo '{group_name}': {data['errors'][0]['message']}"
        )

    return data["data"]["create_group"]["id"]


def populate_board_with_lotes(board_id: int, agrupamentos: dict, token: str):
    for group_name, group_data in agrupamentos.items():

        print(f"📂 Criando grupo: {group_name}")

        group_id = create_group(
            board_id=board_id,
            group_name=group_name,
            token=token
        )

        for lote in group_data["lotes"]:
            create_lote_item(
                board_id=board_id,
                group_id=group_id,
                lote=lote,
                token=token
            )