import os, json
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive"]
ROOT_ID = os.getenv("GOOGLE_DRIVE_ROOT_FOLDER_ID")


def get_drive_service():
    creds = json.loads(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"))
    credentials = service_account.Credentials.from_service_account_info(creds, scopes=SCOPES)
    return build("drive", "v3", credentials=credentials)


def create_folder(service, name, parent):
    folder = service.files().create(
        body={
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent]
        },
        fields="id"
    ).execute()
    return folder["id"]


def create_area_folders(codigo, nome_area, zoneamento, agrupamentos, lotes_totais):
    service = get_drive_service()

    area_name = f"{codigo} {nome_area} - {zoneamento}"
    area_id = create_folder(service, area_name, ROOT_ID)

    for group, info in agrupamentos.items():
        group_id = create_folder(service, group, area_id)
        for lote in info["lotes"]:
            create_folder(service, f"Lote {lote}", group_id)

    return area_id