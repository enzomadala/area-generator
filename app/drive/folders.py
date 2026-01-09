import os
from typing import List
from google.oauth2 import service_account
from googleapiclient.discovery import build

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "service_account.json")

SCOPES = ["https://www.googleapis.com/auth/drive"]

# ID da pasta raiz no Drive
PARENT_FOLDER_ID = "1kMYAs8F05dW3EFLG7Vmje0-DZDdXrpY2"


# --------------------------------------------------
# DRIVE SERVICE
# --------------------------------------------------

def get_drive_service():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        raise FileNotFoundError(
            f"Arquivo service_account.json não encontrado em {SERVICE_ACCOUNT_FILE}"
        )

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )

    return build("drive", "v3", credentials=credentials)


# --------------------------------------------------
# CRIAÇÃO DE PASTAS
# --------------------------------------------------

def create_area_folders(
    codigo: str,
    nome_area: str,
    zoneamento: str,
    agrupamentos: dict,
    lotes_totais: List[int]
) -> dict:
    service = get_drive_service()

    area_name = f"{codigo} {nome_area} - {zoneamento}"

    # Pasta principal da área
    area_folder = service.files().create(
        body={
            "name": area_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [PARENT_FOLDER_ID],
        },
        fields="id"
    ).execute()

    area_folder_id = area_folder["id"]

    # Caso simples: sem agrupamentos
    if not agrupamentos:
        for lote in lotes_totais:
            service.files().create(
                body={
                    "name": str(lote),
                    "mimeType": "application/vnd.google-apps.folder",
                    "parents": [area_folder_id],
                }
            ).execute()

        return {"area_folder_id": area_folder_id}

    # Caso com agrupamentos
    for nome_grupo, dados in agrupamentos.items():
        grupo_folder = service.files().create(
            body={
                "name": nome_grupo,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [area_folder_id],
            },
            fields="id"
        ).execute()

        grupo_id = grupo_folder["id"]

        for lote in dados["lotes"]:
            service.files().create(
                body={
                    "name": str(lote),
                    "mimeType": "application/vnd.google-apps.folder",
                    "parents": [grupo_id],
                }
            ).execute()

    return {"area_folder_id": area_folder_id}