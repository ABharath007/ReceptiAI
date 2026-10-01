from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session


@dataclass
class AgentContext:
    db: Session
    business_id: int

    customer_id: Optional[int] = None
    customer_phone: Optional[str] = None

    session_id: Optional[int] = None