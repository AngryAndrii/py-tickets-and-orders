from django.contrib.auth import get_user_model

from db.models import User


def create_user(username: str,
                password: str,
                first_name: str,
                last_name: str,
                email: str = None,
                ) -> None:
    get_user_model().objects.create_user(username=username,
                                         password=password,
                                         email=email,
                                         first_name=first_name,
                                         last_name=last_name)


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(pk=user_id)


def update_user(user_id: int,
                password: str,
                email: str,
                first_name: str,
                last_name: str,
                username: str = None) -> None:
    user = get_user(user_id)
    user.set_password(password)
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.username = username
    user.save()
