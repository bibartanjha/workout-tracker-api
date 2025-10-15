from typing import Optional

from pydantic import BaseModel
from datetime import date

class WorkoutPlanDay(BaseModel):
    exercise: str
    day_number: int
    plan_day_description: str
    date_completed: Optional[date] = None