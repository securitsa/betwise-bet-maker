from dataclasses import dataclass

from domain.value_objects.role import Role, Roles


@dataclass
class User:
    token: str
    roles: list[Role]

    def is_admin(self):
        return Roles.ADMIN in self.roles
