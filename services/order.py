from django.contrib.auth import get_user_model

from services.user import get_user


def create_order(tickets: list[dict],
                 username: str,
                 date = None) -> None:
    user = get_user_model().objects.get(username=username)

