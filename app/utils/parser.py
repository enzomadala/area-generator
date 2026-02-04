def parse_lotes(text: str) -> list[int]:
    if not text:
        return []
    return sorted({int(x.strip()) for x in text.replace(";", ",").split(",") if x.strip().isdigit()})


def parse_payload(payload: dict) -> dict:
    event = payload["event"]
    cols = event["columnValues"]

    codigo = cols["short_text7oz7a7oh"]["value"]
    nome_area = cols["short_textofxi61f1"]["value"]
    zoneamento = cols["single_selectnlw6vqs"]["label"]["text"]
    tipo_area = cols["single_selectr9ae201"]["label"]["text"]

    lotes_totais = parse_lotes(cols.get("long_textkidkii73", {}).get("text", ""))

    agrupamentos: dict[str, dict] = {}
    lotes_consumidos: set[int] = set()

    # --------------------------------------------------
    # CONDOMÍNIOS
    # --------------------------------------------------
    # Campo padrão: long_textaq7lqsp3
    # Ex: "CD05: 0124,0125,0126"
    if "CONDOMÍNIO" in tipo_area:
        raw_cond = cols.get("long_textaq7lqsp3", {}).get("text", "")

        if raw_cond:
            for bloco in raw_cond.split("\n"):
                if ":" not in bloco:
                    continue

                nome, lotes_txt = bloco.split(":", 1)
                lotes = parse_lotes(lotes_txt)

                agrupamentos[f"Condomínio - {nome.strip()}"] = {
                    "lotes": lotes
                }
                lotes_consumidos.update(lotes)

    # --------------------------------------------------
    # VILAS
    # --------------------------------------------------
    # Ajuste os IDs se forem diferentes no seu board
    if "VILA" in tipo_area:
        vila_nome = cols.get("long_textiiu35ze7", {}).get("text", "").strip() or "Vila"
        lotes_vila = parse_lotes(cols.get("long_textvmy33h5o", {}).get("text", ""))

        if lotes_vila:
            agrupamentos[f"Vila - {vila_nome}"] = {
                "lotes": lotes_vila
            }
            lotes_consumidos.update(lotes_vila)

    # --------------------------------------------------
    # ÁREA PADRÃO (RESIDUAL)
    # --------------------------------------------------
    lotes_padrao = [l for l in lotes_totais if l not in lotes_consumidos]

    if lotes_padrao:
        agrupamentos["Área Padrão"] = {
            "lotes": lotes_padrao
        }

    # --------------------------------------------------
    # USER QUE ENVIOU
    # --------------------------------------------------
    sender_user_id = (
        cols["peoplel58mn9a9"]["personsAndTeams"][0]["id"]
        if "peoplel58mn9a9" in cols
        else event.get("userId")
    )

    return {
        "codigo": codigo,
        "nome_area": nome_area,
        "zoneamento": zoneamento,
        "tipo_area": tipo_area,
        "lotes_totais": lotes_totais,
        "agrupamentos": agrupamentos,
        "sender_user_id": sender_user_id
    }