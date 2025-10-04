from pydantic import BaseModel
from typing import List, Optional

from datetime import date

class ExerciseSet(BaseModel):
    weight: Optional[float] = None
    reps: Optional[int] = None

class Workout(BaseModel):
    exercise: str
    date: date
    sets: List[ExerciseSet] = []
    notes: Optional[str] = None


