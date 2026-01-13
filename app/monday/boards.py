import requests
from app.monday.groups import create_group
from app.monday.items import create_lote_item

MONDAY_API_URL = "https://api.monday.com/v2"


def get_board_groups(board_id: int, token: str) -> list:
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

    response = requests.post(
        MONDAY_API_URL,
        json={"query": query, "variables": {"board_id": board_id}},
        headers={"Authorization": token}
    ).json()

    return response["data"]["boards"][0]["groups"]


def create_item(board_id: int, group_id: str, name: str, token: str):
    query = """
    mutation ($board_id: ID!, $group_id: String!, $item_name: String!) {
        create_item(
            board_id: $board_id,
            group_id: $group_id,
            item_name: $item_name
        ) {
            id
        }
    }
    """

    variables = {
        "board_id": board_id,
        "group_id": group_id,
        "item_name": name
    }

    response = requests.post(
        MONDAY_API_URL,
        json={"query": query, "variables": variables},
        headers={"Authorization": token}
    ).json()

    if "errors" in response:
        raise RuntimeError(response["errors"])


def populate_board_with_lotes(
    board_id: int,
    agrupamentos: dict,
    token: str
):
    groups = get_board_groups(board_id, token)

    # 🔹 Primeiro group do board = Área Padrão
    default_group_id = groups[0]["id"]

    group_map = {
        "Área Padrão": default_group_id
    }

    # 🔹 Cria apenas os groups adicionais
    for group_name in agrupamentos.keys():
        if group_name != "Área Padrão":
            group_map[group_name] = create_group(
                board_id,
                group_name,
                token
            )

    # 🔹 Criação dos items
    for group_name, data in agrupamentos.items():
        group_id = group_map[group_name]

        for lote in data["lotes"]:
            create_item(
                board_id,
                group_id,
                f"Lote {lote}",
                token
            )