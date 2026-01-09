def parse_payload(payload: dict) -> dict:
    event = payload.get("event", {})
    columns = event.get("columnValues")

    if not columns:
        raise Exception("Payload inválido: sem columnValues")

    def text(col_id):
        return columns.get(col_id, {}).get("value", "").strip()

    def label(col_id):
        return columns.get(col_id, {}).get("label", {}).get("text")

    codigo = text("short_text7oz7a7oh")
    nome_area = text("short_textofxi61f1")
    zoneamento = label("single_selectnlw6vqs")
    tipo_area = label("single_selectr9ae201")

    lotes_raw = columns.get("long_textkidkii73", {}).get("text", "")
    lotes = [int(x.strip()) for x in lotes_raw.split(",") if x.strip().isdigit()]

    return {
        "codigo": codigo,
        "nome_area": nome_area,
        "zoneamento": zoneamento,
        "tipo_area": tipo_area,
        "lotes_totais": lotes,
        "agrupamentos": {}
    }