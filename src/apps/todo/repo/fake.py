from typing import Dict
from sqlalchemy.orm import Session

from ..models.domain.todos import *

todos_repo: Dict[str, TodoItem] = {}
