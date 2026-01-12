import os

DEFAULT_TOKEN = os.getenv("MONDAY_TOKEN")

def get_token_for_user(user_id: int) -> str:
    """
    Retorna o token correto baseado no user_id do evento.
    - user_id == -6 → formulário / automação → token padrão
    - user_id >= 0 → token específico do usuário
    """

    # 🔹 Evento vindo de formulário / automação
    if user_id == -6:
        if not DEFAULT_TOKEN:
            raise RuntimeError("MONDAY_TOKEN padrão não configurado")
        return DEFAULT_TOKEN

    env_key = f"MONDAY_TOKEN_{user_id}"
    token = os.getenv(env_key)

    if not token:
        raise RuntimeError(
            f"Token não configurado para user_id {user_id} ({env_key})"
        )

    return token