from typing import Protocol

import bcrypt


class IPasswordHasher(Protocol):
    def hash(
        self,
        raw_password: str,
    ) -> str: ...

    def verify(
        self,
        raw_password: str,
        hashed_password: str,
    ) -> bool: ...


class BcryptPasswordHasher(IPasswordHasher):
    def hash(
        self,
        raw_password: str,
    ):
        salt: bytes = bcrypt.gensalt()
        hashed: bytes = bcrypt.hashpw(
            password=raw_password.encode("utf-8"),
            salt=salt,
        )

        return hashed.decode("utf-8")

    def verify(
        self,
        raw_password: str,
        hashed_password: str,
    ) -> bool:
        return bcrypt.checkpw(
            password=raw_password.encode("utf-8"),
            hashed_password=hashed_password.encode("utf-8"),
        )
