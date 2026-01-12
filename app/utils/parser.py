def parse_payload(payload: dict) -> dict:
    event = payload.get("event", {})
    column_values = event.get("columnValues", {})

    # Campos do formulário
    codigo = column_values["short_text7oz7a7oh"]["value"]
    nome_area = column_values["short_textofxi61f1"]["value"]
    zoneamento = column_values["single_selectnlw6vqs"]["label"]["text"]
    tipo_area = column_values["single_selectr9ae201"]["label"]["text"]

    lotes_raw = column_values["long_textkidkii73"]["text"]
    lotes_totais = [int(x.strip()) for x in lotes_raw.split(",") if x.strip().isdigit()]

    # 🔹 QUEM ENVIOU O FORMULÁRIO (coluna people)
    sender_column = column_values.get("peoplel58mn9a9", {})
    sender_list = sender_column.get("personsAndTeams", [])

    sender_user_id = None
    if sender_list:
        sender_user_id = sender_list[0]["id"]

    return {
        "codigo": codigo,
        "nome_area": nome_area,
        "zoneamento": zoneamento,
        "tipo_area": tipo_area,
        "lotes_totais": lotes_totais,
        "agrupamentos": {},
        "sender_user_id": sender_user_id,
    }