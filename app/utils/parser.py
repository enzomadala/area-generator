def parse_lotes(text: str) -> list[int]:
    if not text:
        return []

    return [
        int(l.strip())
        for l in text.split(",")
        if l.strip().isdigit()
    ]


def parse_condominios(text: str) -> dict:
    grupos = {}

    if not text:
        return grupos

    for line in text.splitlines():
        if ":" not in line:
            continue

        nome, lotes = line.split(":", 1)
        grupos[f"Condomínio - {nome.strip()}"] = {
            "lotes": parse_lotes(lotes)
        }

    return grupos


def parse_payload(payload: dict) -> dict:
    cols = payload["event"]["columnValues"]

    tipo_area = cols["single_selectr9ae201"]["label"]["text"]

    agrupamentos = {}
    lotes_totais = set()

    # 🔹 Área padrão
    if "ÁREA PADRÃO" in tipo_area:
        lotes = parse_lotes(cols["long_textkidkii73"]["text"])
        agrupamentos["Área Padrão"] = {"lotes": lotes}
        lotes_totais.update(lotes)

    # 🔹 Vila
    if "VILA" in tipo_area:
        nome_vila = cols["long_textiiu35ze7"]["text"]
        lotes_vila = parse_lotes(cols["long_textvmy33h5o"]["text"])

        if nome_vila:
            key = f"Vila - {nome_vila}"
            agrupamentos[key] = {"lotes": lotes_vila}
            lotes_totais.update(lotes_vila)

    # 🔹 Condomínio
    if "CONDOMÍNIO" in tipo_area:
        # múltiplos condomínios
        if tipo_area == "SOMENTE CONDOMÍNIOS":
            grupos = parse_condominios(cols["long_textaq7lqsp3"]["text"])
            agrupamentos.update(grupos)

            for g in grupos.values():
                lotes_totais.update(g["lotes"])

        # único condomínio
        else:
            nome = cols["short_textwh526rz4"]["value"]
            lotes = parse_lotes(cols["long_textqwhsfkab"]["text"])

            key = f"Condomínio - {nome}"
            agrupamentos[key] = {"lotes": lotes}
            lotes_totais.update(lotes)

    return {
        "codigo": cols["short_text7oz7a7oh"]["value"],
        "nome_area": cols["short_textofxi61f1"]["value"],
        "zoneamento": cols["single_selectnlw6vqs"]["label"]["text"],
        "tipo_area": tipo_area,
        "agrupamentos": agrupamentos,
        "lotes_totais": sorted(lotes_totais)
    }