import os
from fastapi import FastAPI, Body
from dotenv import load_dotenv

load_dotenv()

print(">>> MAIN.PY CARREGADO <<<")

app = FastAPI()

from app.utils.parser import parse_payload
from app.drive.folders import create_area_folders
from app.monday.boards import duplicate_board, populate_board_with_lotes
from app.monday.status import set_status
from app.monday.links import update_link_column
from app.monday.auth import get_token_for_user
from app.monday.groups import create_group
from app.monday.items import create_lote_item


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

TEMPLATE_BOARD_ID_RAW = os.getenv("MONDAY_TEMPLATE_BOARD_ID")

if not TEMPLATE_BOARD_ID_RAW:
    raise RuntimeError("Variável MONDAY_TEMPLATE_BOARD_ID não configurada")

TEMPLATE_BOARD_ID = int(TEMPLATE_BOARD_ID_RAW)

STATUS_COLUMN_ID = "color_mkzdtnz7"
BOARD_LINK_COLUMN_ID = "link_mkzeye6w"
DRIVE_LINK_COLUMN_ID = "link_mkzetwpb"

# --------------------------------------------------
# ENDPOINT
# --------------------------------------------------

@app.post("/nova-area")
async def nova_area(payload: dict = Body(...)):
    print("\n🚀 Nova requisição /nova-area")
    print("📦 PAYLOAD:", payload)

    # 🔹 Handshake Monday
    if "challenge" in payload:
        return {"challenge": payload["challenge"]}

    event = payload.get("event", {})
    column_values = event.get("columnValues")

    if not column_values:
        print("⚠️ Evento ignorado (sem columnValues)")
        return {"status": "ignored"}

    # 🔹 Parse
    data = parse_payload(payload)
    print("🧠 DADOS PARSEADOS:", data)

    sender_user_id = data["sender_user_id"]

    # 🔹 TOKEN DO USUÁRIO QUE ENVIOU
    token = get_token_for_user(sender_user_id)

    form_board_id = event["boardId"]
    form_item_id = event["pulseId"]

    # 🔹 Status → processando
    set_status(
        board_id=form_board_id,
        item_id=form_item_id,
        label="🕓 Em processamento",
        token=token
    )

    # 🔹 Drive
    drive_area_id = create_area_folders(
    codigo=data["codigo"],
    nome_area=data["nome_area"],
    zoneamento=data["zoneamento"],
    agrupamentos=data["agrupamentos"]
)

    # 🔹 Board (CRIA COM OWNER CORRETO)
    board_name = f"{data['codigo']} {data['nome_area']} - {data['zoneamento']}"

    new_board_id = duplicate_board(
        TEMPLATE_BOARD_ID,
        board_name,
        token
    )

    populate_board_with_lotes(
        board_id=new_board_id,
        agrupamentos=data["agrupamentos"],
        token=token
    )

    # 🔹 Links no formulário
    update_link_column(
        board_id=form_board_id,
        item_id=form_item_id,
        column_id=BOARD_LINK_COLUMN_ID,
        url=f"https://madalainc.monday.com/boards/{new_board_id}",
        text="Board da Área",
        token=token
    )

    update_link_column(
        board_id=form_board_id,
        item_id=form_item_id,
        column_id=DRIVE_LINK_COLUMN_ID,
        url=f"https://drive.google.com/drive/folders/{drive_area_id}",
        text="Pasta no Drive",
        token=token
    )

    # 🔹 Status → sucesso
    set_status(
        board_id=form_board_id,
        item_id=form_item_id,
        label="✅ Área criada",
        token=token
    )

    print("✅ ÁREA CRIADA COM SUCESSO")
    return {"status": "ok"}