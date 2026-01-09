import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Escopo completo do Drive
SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_drive_service():
    """
    Cria o serviço do Google Drive a partir da variável de ambiente
    GOOGLE_SERVICE_ACCOUNT_JSON
    """

    service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

    if not service_account_json:
        raise RuntimeError(
            "Variável de ambiente GOOGLE_SERVICE_ACCOUNT_JSON não configurada"
        )

    try:
        credentials_info = json.loads(service_account_json)
    except json.JSONDecodeError:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON não é um JSON válido")

    credentials = service_account.Credentials.from_service_account_info(
        credentials_info,
        scopes=SCOPES
    )

    return build("drive", "v3", credentials=credentials)


def create_folder(service, name, parent_id=None):
    """
    Cria uma pasta no Google Drive.
    Se parent_id for None, cria na raiz do Drive.
    """

    file_metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }

    if parent_id:
        file_metadata["parents"] = [parent_id]

    folder = service.files().create(
        body=file_metadata,
        fields="id"
    ).execute()

    return folder["id"]


def create_area_folders(
    codigo: str,
    nome_area: str,
    lotes_totais: list[int],
):
    """
    Estrutura final:

    /ÁREAS
        /000123 - Nome da Área
            /Lotes
                /Lote 1
                /Lote 2
                ...
    """

    try:
        service = get_drive_service()

        # 🔹 Pasta raiz fixa
        ROOT_FOLDER_NAME = "ÁREAS"

        # Procura se a pasta ÁREAS já existe
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

        if results.get("files"):
            root_folder_id = results["files"][0]["id"]
        else:
            root_folder_id = create_folder(service, ROOT_FOLDER_NAME)

        # 🔹 Pasta da área
        area_folder_name = f"{codigo} - {nome_area}"
        area_folder_id = create_folder(
            service,
            area_folder_name,
            root_folder_id
        )

        # 🔹 Pasta Lotes
        lotes_folder_id = create_folder(
            service,
            "Lotes",
            area_folder_id
        )

        # 🔹 Pastas de cada lote
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
        raise RuntimeError(f"Erro ao criar pastas no Drive: {e}")