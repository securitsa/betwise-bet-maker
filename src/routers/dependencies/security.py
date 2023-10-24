from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from domain.value_objects.role import Roles
from domain.value_objects.user import User
from usecases.security.security_usecase import SecurityUsecase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def get_security_usecase(token: str = Depends(oauth2_scheme)) -> SecurityUsecase:
    return SecurityUsecase(token)


def get_user_from_access_token(security_usecase=Depends(get_security_usecase)) -> User:
    return security_usecase.get_user()


def admin_authorizer(security_usecase: SecurityUsecase = Depends(get_security_usecase)):
    return security_usecase.check_roles([Roles.ADMIN])


def admin_user_authorizer(security_usecase: SecurityUsecase = Depends(get_security_usecase)):
    return security_usecase.check_roles([Roles.ADMIN, Roles.USER])
