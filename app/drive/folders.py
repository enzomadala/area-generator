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

ROOT_FOLDER_NAME = "ÁREAS"


# --------------------------------------------------
# DRIVE SERVICE
# --------------------------------------------------

def get_drive_service():
    """
    Cria o serviço do Google Drive a partir da variável de ambiente
    GOOGLE_SERVICE_ACCOUNT_JSON (JSON completo da service account).
    """

    service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

    if not service_account_json:
        raise RuntimeError(
            "Variável de ambiente GOOGLE_SERVICE_ACCOUNT_JSON não configurada"
        )

    try:
        credentials_info = json.loads(service_account_json)
    except json.JSONDecodeError:
        raise RuntimeError(
            "GOOGLE_SERVICE_ACCOUNT_JSON não contém um JSON válido"
        )

    credentials = service_account.Credentials.from_service_account_info(
        credentials_info,
        scopes=SCOPES
    )

    return build("drive", "v3", credentials=credentials)


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def create_folder(service, name: str, parent_id: str | None = None) -> str:
    """
    Cria uma pasta no Google Drive e retorna o ID.
    """

    metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }

    if parent_id:
        metadata["parents"] = [parent_id]

    folder = service.files().create(
        body=metadata,
        fields="id"
    ).execute()

    return folder["id"]


def get_or_create_root_folder(service) -> str:
    """
    Busca a pasta raiz 'ÁREAS'. Se não existir, cria.
    """

    query = (
        f"name = '{ROOT_FOLDER_NAME}' and "
        "mimeType = 'application/vnd.google-apps.folder' and "
        "trashed = false"
    )

    results = service.files().list(
        q=query,
        fields="files(id, name)",
        spaces="drive"
    ).execute()

    files = results.get("files", [])

    if files:
        return files[0]["id"]

    return create_folder(service, ROOT_FOLDER_NAME)


# --------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------

def create_area_folders(
    codigo: str,
    nome_area: str,
    zoneamento: str,
    agrupamentos: Dict,
    lotes_totais: List[int]
) -> Dict[str, str]:
    """
    Estrutura criada no Drive:

    /ÁREAS
        /000123 - Nome da Área (ZEU)
            /Lotes
                /Lote 1
                /Lote 2
                ...
    """

    try:
        service = get_drive_service()

        # 🔹 Pasta raiz
        root_folder_id = get_or_create_root_folder(service)

        # 🔹 Pasta da área (com zoneamento)
        area_folder_name = f"{codigo} - {nome_area} ({zoneamento})"
        area_folder_id = create_folder(
            service,
            area_folder_name,
            root_folder_id
        )

        # 🔹 Pasta "Lotes"
        lotes_folder_id = create_folder(
            service,
            "Lotes",
            area_folder_id
        )

        # 🔹 Criação dos lotes
        for lote in lotes_totais:
            create_folder(
                service,
                f"Lote {lote}",
                lotes_folder_id
            )

        return {
            "root_folder_id": root_folder_id,
            "area_folder_id": area_folder_id,
            "lotes_folder_id": lotes_folder_id,
        }

    except HttpError as e:
        raise RuntimeError(
            f"Erro ao criar estrutura de pastas no Google Drive: {e}"
        )