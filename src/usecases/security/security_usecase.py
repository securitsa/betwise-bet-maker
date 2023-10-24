from jose import jwt

from core.exceptions.auth_exceptions import InvalidJwtToken, NotAuthorizedException
from domain.value_objects.role import Role
from domain.value_objects.user import User


class SecurityUsecase:
    def __init__(self, user_token: str):
        claims = self.__check_claims(user_token)
        self.user = User(claims["iss"], [Role(role) for role in claims["roles"]])

    @staticmethod
    def __check_claims(user_token: str) -> dict:
        claims = jwt.get_unverified_claims(user_token)
        if "iss" not in claims or "roles" not in claims:
            raise InvalidJwtToken
        return claims

    def get_user(self) -> User:
        return self.user

    def check_roles(self, allowed_roles: list[Role]):
        roles = [role.name.lower() for role in self.user.roles]
        if len(list(set(roles) & set([role.name.lower() for role in allowed_roles]))) == 0:
            raise NotAuthorizedException
