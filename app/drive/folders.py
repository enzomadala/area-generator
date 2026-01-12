import os
import json
from typing import List, Dict
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SCOPES = ["https://www.googleapis.com/auth/drive"]


# --------------------------------------------------
# DRIVE SERVICE
# --------------------------------------------------

def get_drive_service():
    service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

    if not service_account_json:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON não configurada")

    credentials_info = json.loads(service_account_json)

    credentials = service_account.Credentials.from_service_account_info(
        credentials_info,
        scopes=SCOPES
    )

    return build("drive", "v3", credentials=credentials)


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def create_folder(service, name: str, parent_id: str) -> str:
    metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }

    folder = service.files().create(
        body=metadata,
        fields="id"
    ).execute()

    return folder["id"]


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def create_area_folders(
    codigo: str,
    nome_area: str,
    zoneamento: str,
    agrupamentos: Dict,
    lotes_totais: List[int]
) -> Dict[str, str]:
    """
    Estrutura criada:

    MONDAY (ID fixo)
      └── 000123 - Nome da Área (ZEU)
          └── Lotes
              └── Lote 1
    """

    try:
        service = get_drive_service()

        root_folder_id = os.getenv("GOOGLE_DRIVE_ROOT_FOLDER_ID")
        if not root_folder_id:
            raise RuntimeError("GOOGLE_DRIVE_ROOT_FOLDER_ID não configurada")

        # Pasta da área
        area_folder_name = f"{codigo} - {nome_area} ({zoneamento})"
        area_folder_id = create_folder(
            service,
            area_folder_name,
            root_folder_id
        )

        # Pasta Lotes
        lotes_folder_id = create_folder(
            service,
            "Lotes",
            area_folder_id
        )

        # Subpastas dos lotes
        for lote in lotes_totais:
            create_folder(
                service,
                f"Lote {lote}",
                lotes_folder_id
            )

        return {
            "area_folder_id": area_folder_id,
            "lotes_folder_id": lotes_folder_id,
        }

    except HttpError as e:
        raise RuntimeError(f"Erro ao criar pastas no Drive: {e}")