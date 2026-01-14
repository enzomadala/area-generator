import os


def get_token_for_user(user_id: int) -> str:
    env_key = f"MONDAY_TOKEN_{user_id}"
    token = os.getenv(env_key)

    if not token:
        raise RuntimeError(f"Token não configurado para user_id {user_id}")

    return token