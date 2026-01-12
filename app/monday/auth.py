import os


def get_token_for_user(user_id: int) -> str:
    """
    Busca o token do Monday com base no userId do evento.
    Ex: user_id = 27452153 → MONDAY_TOKEN_27452153
    """

    env_key = f"MONDAY_TOKEN_{user_id}"
    token = os.getenv(env_key)

    if not token:
        raise RuntimeError(
            f"Token não configurado para user_id {user_id} ({env_key})"
        )

    return token