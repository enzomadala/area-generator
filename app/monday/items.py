from app.monday.client import monday_request


def get_item_values(item_id: int, token: str) -> dict:
    """
    Busca os valores das colunas de um item no Monday
    Retorna no formato:
    {
        "column_id": {
            "text": "...",
            "value": "...",
            "label": "..."  # apenas status
        }
    }
    """
    query = """
    query ($item_id: [ID!]) {
      items(ids: $item_id) {
        id
        name
        column_values {
          id
          text
          value
          ... on StatusValue {
            label
          }
        }
      }
    }
    """

    variables = {
        "item_id": str(item_id)
    }

    result = monday_request(query, variables, token)

    if "errors" in result:
        raise Exception(f"Erro ao buscar item {item_id}: {result['errors']}")

    item = result["data"]["items"][0]

    columns = {}
    for col in item["column_values"]:
        columns[col["id"]] = {
            "text": col.get("text"),
            "value": col.get("value"),
            "label": col.get("label")
        }

    return columns


def update_text_column(
    item_id: int,
    column_id: str,
    value: str,
    token: str
):
    """
    Atualiza uma coluna de texto simples no Monday
    (ex: BOARD GERADO)
    """
    query = """
    mutation ($item_id: ID!, $column_id: String!, $value: String!) {
      change_simple_column_value(
        item_id: $item_id,
        column_id: $column_id,
        value: $value
      ) {
        id
      }
    }
    """

    variables = {
        "item_id": item_id,
        "column_id": column_id,
        "value": value
    }

    result = monday_request(query, variables, token)

    if "errors" in result:
        raise Exception(result["errors"])


def create_lote_item(board_id, group_id, lote, token):
    query = """
    mutation ($board: Int!, $group: String!, $name: String!) {
      create_item (
        board_id: $board,
        group_id: $group,
        item_name: $name
      ) {
        id
      }
    }
    """

    variables = {
        "board": board_id,
        "group": group_id,
        "name": f"Lote {lote}"
    }

    monday_request(query, variables, token)