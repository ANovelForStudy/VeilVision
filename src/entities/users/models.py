from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(slots=True)
class User:
    id: UUID
    email: str
    full_name: str
    is_active: bool
    created_at: datetime

    @classmethod
    def create(cls, email: str, full_name: str) -> "User":
        return cls(
            id=uuid4(),
            email=email,
            full_name=full_name,
            is_active=True,
            created_at=datetime.utcnow(),
        )
