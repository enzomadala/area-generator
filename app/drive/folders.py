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
ROOT_FOLDER_ID = os.getenv("GOOGLE_DRIVE_ROOT_FOLDER_ID")


def get_drive_service():
    credentials_info = json.loads(
        os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    )

    credentials = service_account.Credentials.from_service_account_info(
        credentials_info,
        scopes=SCOPES
    )

    return build("drive", "v3", credentials=credentials)


def create_folder(service, name: str, parent_id: str) -> str:
    folder = service.files().create(
        body={
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id]
        },
        fields="id"
    ).execute()

    return folder["id"]


def create_area_folders(
    codigo: str,
    nome_area: str,
    zoneamento: str,
    agrupamentos: Dict,
    lotes_totais: List[int]
) -> Dict[str, str]:

    service = get_drive_service()

    area_folder_name = f"{codigo} {nome_area} - {zoneamento}"
    area_folder_id = create_folder(
        service,
        area_folder_name,
        ROOT_FOLDER_ID
    )

    # 🔹 Com agrupamentos
    if agrupamentos:
        for group_name, data in agrupamentos.items():
            group_folder_id = create_folder(
                service,
                group_name,
                area_folder_id
            )

            for lote in data["lotes"]:
                create_folder(
                    service,
                    f"Lote {lote}",
                    group_folder_id
                )
    else:
        # 🔹 Caso simples
        for lote in lotes_totais:
            create_folder(
                service,
                f"Lote {lote}",
                area_folder_id
            )

    return {
        "area_folder_id": area_folder_id
    }