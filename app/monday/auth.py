import os


def get_token_for_user(user_id: int) -> str:
    if not user_id:
        raise RuntimeError("sender_user_id não encontrado no formulário")

    env_key = f"MONDAY_TOKEN_{user_id}"
    token = os.getenv(env_key)

    if not token:
        raise RuntimeError(
            f"Token não configurado para user_id {user_id} ({env_key})"
        )

    return token