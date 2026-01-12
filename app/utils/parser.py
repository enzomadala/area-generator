def parse_lotes(text: str):
    """
    Converte '1,2,3,4' -> [1,2,3,4]
    """
    if not text:
        return []

    return [
        int(x.strip())
        for x in text.split(",")
        if x.strip().isdigit()
    ]


def parse_condominios(text: str):
    """
    Converte:
    CD02: 10,11,12
    CD03: 13,14

    Em:
    {
        "Condomínio - CD02": {"lotes": [10,11,12]},
        "Condomínio - CD03": {"lotes": [13,14]}
    }
    """
    agrupamentos = {}

    if not text:
        return agrupamentos

    linhas = text.splitlines()

    for linha in linhas:
        if ":" not in linha:
            continue

        nome, lotes = linha.split(":", 1)
        nome = nome.strip()
        lotes = parse_lotes(lotes)

        if nome and lotes:
            agrupamentos[f"Condomínio - {nome}"] = {
                "lotes": lotes
            }

    return agrupamentos


def parse_payload(payload: dict) -> dict:
    event = payload.get("event", {})
    column_values = event.get("columnValues", {})

    # --------------------------------------------------
    # CAMPOS BÁSICOS
    # --------------------------------------------------

    codigo = column_values.get("short_text7oz7a7oh", {}).get("value", "")
    nome_area = column_values.get("short_textofxi61f1", {}).get("value", "")
    zoneamento = (
        column_values.get("single_selectnlw6vqs", {})
        .get("label", {})
        .get("text", "")
    )

    tipo_area = (
        column_values.get("single_selectr9ae201", {})
        .get("label", {})
        .get("text", "")
    )

    lotes_totais_text = column_values.get("long_textkidkii73", {}).get("text", "")
    lotes_totais = parse_lotes(lotes_totais_text)

    # --------------------------------------------------
    # SENDER (quem enviou o formulário)
    # --------------------------------------------------

    sender_user_id = None

    people_column = column_values.get("peoplel58mn9a9")
    if people_column:
        persons = people_column.get("personsAndTeams", [])
        if persons:
            sender_user_id = persons[0]["id"]

    # --------------------------------------------------
    # AGRUPAMENTOS
    # --------------------------------------------------

    agrupamentos = {}

    # 🔹 ÁREA PADRÃO
    if "ÁREA PADRÃO" in tipo_area:
        agrupamentos["Área Padrão"] = {
            "lotes": lotes_totais
        }

    # 🔹 SOMENTE CONDOMÍNIOS
    if tipo_area == "SOMENTE CONDOMÍNIOS":
        condominios_text = column_values.get("long_textaq7lqsp3", {}).get("text", "")
        agrupamentos.update(parse_condominios(condominios_text))

    # 🔹 ÁREA PADRÃO + CONDOMÍNIO
    if tipo_area == "ÁREA PADRÃO + CONDOMÍNIO":
        nome_condominio = column_values.get("short_textwh526rz4", {}).get("value", "")
        lotes_condominio_text = column_values.get("long_textqwhsfkab", {}).get("text", "")
        lotes_condominio = parse_lotes(lotes_condominio_text)

        if nome_condominio and lotes_condominio:
            agrupamentos[f"Condomínio - {nome_condominio}"] = {
                "lotes": lotes_condominio
            }

    # 🔹 ÁREA PADRÃO + VILA
    if tipo_area == "ÁREA PADRÃO + VILA":
        nome_vila = column_values.get("long_textiiu35ze7", {}).get("text", "")
        lotes_vila_text = column_values.get("long_textvmy33h5o", {}).get("text", "")
        lotes_vila = parse_lotes(lotes_vila_text)

        if nome_vila and lotes_vila:
            agrupamentos[f"Vila - {nome_vila}"] = {
                "lotes": lotes_vila
            }

    # 🔹 ÁREA PADRÃO + VILA + CONDOMÍNIO
    if tipo_area == "ÁREA PADRÃO + VILA + CONDOMÍNIO":
        nome_condominio = column_values.get("short_textwh526rz4", {}).get("value", "")
        lotes_condominio_text = column_values.get("long_textqwhsfkab", {}).get("text", "")
        lotes_condominio = parse_lotes(lotes_condominio_text)

        nome_vila = column_values.get("long_textiiu35ze7", {}).get("text", "")
        lotes_vila_text = column_values.get("long_textvmy33h5o", {}).get("text", "")
        lotes_vila = parse_lotes(lotes_vila_text)

        if nome_condominio and lotes_condominio:
            agrupamentos[f"Condomínio - {nome_condominio}"] = {
                "lotes": lotes_condominio
            }

        if nome_vila and lotes_vila:
            agrupamentos[f"Vila - {nome_vila}"] = {
                "lotes": lotes_vila
            }

    # --------------------------------------------------
    # RESULTADO FINAL
    # --------------------------------------------------

    return {
        "codigo": codigo,
        "nome_area": nome_area,
        "zoneamento": zoneamento,
        "tipo_area": tipo_area,
        "lotes_totais": lotes_totais,
        "agrupamentos": agrupamentos,
        "sender_user_id": sender_user_id
    }