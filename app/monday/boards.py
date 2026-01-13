import requests
from app.monday.groups import create_group
from app.monday.client import monday_request
from app.monday.groups import create_group, get_default_group
from app.monday.items import create_item

MONDAY_API_URL = "https://api.monday.com/v2"


# --------------------------------------------------
# DUPLICAR BOARD
# --------------------------------------------------

def duplicate_board(template_board_id: int, board_name: str, token: str) -> int:
    query = """
    mutation ($board_id: Int!, $name: String!) {
        duplicate_board(
            board_id: $board_id,
            duplicate_type: duplicate_board_with_structure,
            board_name: $name
        ) {
            board {
                id
            }
        }
    }
    """

    variables = {
        "board_id": template_board_id,
        "name": board_name
    }

    response = monday_request(query, variables, token)

    if "errors" in response:
        raise RuntimeError(response["errors"])

    return int(response["data"]["duplicate_board"]["board"]["id"])


# --------------------------------------------------
# GROUPS
# --------------------------------------------------

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


# --------------------------------------------------
# ITEMS
# --------------------------------------------------

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


# --------------------------------------------------
# POPULAR BOARD
# --------------------------------------------------

def populate_board_with_lotes(
    board_id: int,
    agrupamentos: dict,
    token: str
):
    default_group_id = get_default_group(board_id, token)
    group_map = {}

    for group_name, info in agrupamentos.items():
        if group_name == "Área Padrão":
            group_id = default_group_id
        else:
            group_id = create_group(board_id, group_name, token)

        group_map[group_name] = group_id

        for lote in info["lotes"]:
            create_item(
                board_id=board_id,
                group_id=group_id,
                item_name=f"Lote {lote}",
                token=token
            )

    # 🔹 Criar apenas grupos adicionais
    for group_name in agrupamentos.keys():
        if group_name != "Área Padrão":
            group_map[group_name] = create_group(
                board_id,
                group_name,
                token
            )

    # 🔹 Criar items
    for group_name, data in agrupamentos.items():
        group_id = group_map[group_name]

        for lote in data["lotes"]:
            create_item(
                board_id,
                group_id,
                f"Lote {lote}",
                token
            )