from app.monday.client import monday_request


def create_groups(board_id: int, agrupamentos: dict, token: str) -> dict:
    group_map = {}

    for nome_grupo in agrupamentos.keys():
        query = """
        mutation ($board_id: ID!, $group_name: String!) {
          create_group(board_id: $board_id, group_name: $group_name) {
            id
          }
        }
        """

        variables = {
            "board_id": board_id,
            "group_name": nome_grupo
        }

        result = monday_request(query, variables, token)

        if "errors" in result:
            raise Exception(f"Erro ao criar grupo '{nome_grupo}': {result['errors']}")

        group_map[nome_grupo] = result["data"]["create_group"]["id"]

    return group_map
