import requests
from app.monday.groups import create_group

MONDAY_API_URL = "https://api.monday.com/v2"


# --------------------------------------------------
# DUPLICAR BOARD
# --------------------------------------------------

def duplicate_board(
    template_board_id: int,
    board_name: str,
    token: str
) -> int:
    query = """
    mutation ($board_id: ID!, $board_name: String!) {
        duplicate_board(
            board_id: $board_id,
            board_name: $board_name,
            duplicate_type: with_structure
        ) {
            board {
                id
            }
        }
    }
    """

    variables = {
        "board_id": template_board_id,
        "board_name": board_name
    }

    response = requests.post(
        MONDAY_API_URL,
        json={"query": query, "variables": variables},
        headers={"Authorization": token}
    ).json()

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
    groups = get_board_groups(board_id, token)

    # 🔹 Primeiro grupo nativo = Área Padrão
    default_group_id = groups[0]["id"]

    group_map = {
        "Área Padrão": default_group_id
    }

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