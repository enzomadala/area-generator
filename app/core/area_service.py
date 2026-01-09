from app.drive.folders import create_area_folders
from app.monday.boards import (
    duplicate_board,
    populate_board_with_lotes
)


def processar_area(
    *,
    data: dict,
    token: str,
    template_board_id: int
):
    """
    Fluxo único de criação de área:
    - Drive
    - Board
    - Itens
    """

    # 📁 Drive
    drive_result = create_area_folders(
        codigo=data["codigo"],
        nome_area=data["nome_area"],
        zoneamento=data["zoneamento"],
        agrupamentos=data["agrupamentos"],
        lotes_totais=data["lotes_totais"]
    )

    # 📋 Board
    board_name = f"{data['codigo']} - {data['nome_area']}"
    new_board_id = duplicate_board(
        template_board_id,
        board_name,
        token=token
    )

    # 📦 Itens
    populate_board_with_lotes(
        board_id=new_board_id,
        agrupamentos=data["agrupamentos"],
        lotes_totais=data["lotes_totais"],
        token=token
    )

    return {
        "board_id": new_board_id,
        "drive": drive_result
    }