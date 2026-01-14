def parse_lotes(text: str) -> list[int]:
    if not text:
        return []
    return sorted({int(x.strip()) for x in text.split(",") if x.strip().isdigit()})


def parse_payload(payload: dict) -> dict:
    event = payload["event"]
    cols = event["columnValues"]

    codigo = cols["short_text7oz7a7oh"]["value"]
    nome_area = cols["short_textofxi61f1"]["value"]
    zoneamento = cols["single_selectnlw6vqs"]["label"]["text"]
    tipo_area = cols["single_selectr9ae201"]["label"]["text"]

    lotes_totais = parse_lotes(cols["long_textkidkii73"]["text"])

    agrupamentos = {}
    lotes_consumidos = set()

    # 🔹 Condomínio
    if "CONDOMÍNIO" in tipo_area:
        codigo_cond = cols["short_textwh526rz4"]["value"]
        lotes_cond = parse_lotes(cols["long_textqwhsfkab"]["text"])
        agrupamentos[f"Condomínio - {codigo_cond}"] = {"lotes": lotes_cond}
        lotes_consumidos.update(lotes_cond)

    # 🔹 Vila
    if "VILA" in tipo_area:
        vila_nome = cols.get("short_text_vila", {}).get("value", "Vila")
        lotes_vila = parse_lotes(cols.get("long_text_vila", {}).get("text", ""))
        agrupamentos[f"Vila - {vila_nome}"] = {"lotes": lotes_vila}
        lotes_consumidos.update(lotes_vila)

    # 🔹 Área padrão (residual)
    lotes_padrao = [l for l in lotes_totais if l not in lotes_consumidos]
    agrupamentos["Área Padrão"] = {"lotes": lotes_padrao}

    return {
        "codigo": codigo,
        "nome_area": nome_area,
        "zoneamento": zoneamento,
        "tipo_area": tipo_area,
        "lotes_totais": lotes_totais,
        "agrupamentos": agrupamentos,
        "sender_user_id": event["columnValues"]["peoplel58mn9a9"]["personsAndTeams"][0]["id"]
    }