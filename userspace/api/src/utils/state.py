from dataclasses import dataclass
from typing import Optional


@dataclass
class State:
    mode: Optional[str] = None


alfred_state = State()
