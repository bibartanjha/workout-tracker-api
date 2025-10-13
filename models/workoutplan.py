from typing import Optional

from pydantic import BaseModel
from datetime import date

class WorkoutPlan(BaseModel):
    exercise: str
    day_number: int
    completed: bool = False
    date_completed: Optional[date] = None