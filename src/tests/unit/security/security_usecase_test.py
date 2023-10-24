from contextlib import nullcontext as does_not_raise

import pytest
from jose import jwt

from core.exceptions.auth_exceptions import InvalidJwtToken, NotAuthorizedException
from domain.value_objects.role import Role, Roles
from domain.value_objects.user import User
from usecases.security.security_usecase import SecurityUsecase

USER_TOKEN = "user_token"
ITINERARY_TOKE = "itinerary_token"


def create_jwt_token(user_token: str = None, roles: list[Role] = None):
    payload = {}
    if user_token is not None:
        payload.update({"iss": user_token})
    if roles is not None:
        payload.update({"roles": [role.name for role in roles]})
    return jwt.encode(payload, "super_secret_key", algorithm="HS256")


@pytest.mark.asyncio
@pytest.mark.parametrize("jwt_token", [create_jwt_token(user_token=USER_TOKEN), create_jwt_token(roles=[Roles.USER])])
async def test_no_iss_or_roles_in_jwt_token(jwt_token):
    with pytest.raises(InvalidJwtToken):
        SecurityUsecase(jwt_token)


@pytest.mark.asyncio
async def test_user_from_jwt_token_success():
    user = User(token=USER_TOKEN, roles=[Roles.USER])
    security_usecase = SecurityUsecase(create_jwt_token(user_token=user.token, roles=user.roles))
    assert security_usecase.get_user() == user


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "jwt_token, allowed_roles, exception",
    [
        (create_jwt_token(user_token=USER_TOKEN, roles=[Roles.USER]), [Roles.USER], does_not_raise()),
        (create_jwt_token(user_token=USER_TOKEN, roles=[Roles.ADMIN]), [Roles.ADMIN], does_not_raise()),
        (
            create_jwt_token(user_token=USER_TOKEN, roles=[Roles.ADMIN]),
            [Roles.USER],
            pytest.raises(NotAuthorizedException),
        ),
    ],
)
async def test_check_roles(jwt_token, allowed_roles, exception):
    security_usecase = SecurityUsecase(jwt_token)
    with exception:
        assert security_usecase.check_roles(allowed_roles) is None
