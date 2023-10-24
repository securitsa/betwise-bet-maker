from dataclasses import dataclass


@dataclass
class Role:
    name: str


class Roles:
    ADMIN = Role("ADMIN")
    USER = Role("USER")
