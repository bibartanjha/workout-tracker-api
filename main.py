from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from typing import List, Optional

import datetime
from datetime import date
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
app = FastAPI()

class Workout(BaseModel):
    exercise: str
    date: datetime.date = None
    set1_weight: Optional[float] = None
    set1_reps: Optional[int] = None
    set2_weight: Optional[float] = None
    set2_reps: Optional[int] = None
    set3_weight: Optional[float] = None
    set3_reps: Optional[int] = None
    set4_weight: Optional[float] = None
    set4_reps: Optional[int] = None
    set5_weight: Optional[float] = None
    set5_reps: Optional[int] = None
    warmup_weight: Optional[float] = None
    warmup_reps: Optional[int] = None
    notes: Optional[str] = None

    def valueswithlabels(self):
        valuesList = [f"Exercise: {self.exercise}", f"Date: {self.date}"]
        if (self.warmup_weight is not None) and (self.warmup_reps is not None):
            valuesList.append(f"Warm-up: {self.warmup_weight} - {self.warmup_reps} reps")
        if (self.set1_weight is not None) and (self.set1_reps is not None):
            valuesList.append(f"Set 1: {self.set1_weight} - {self.set1_reps} reps")
        if (self.set2_weight is not None) and (self.set2_reps is not None):
            valuesList.append(f"Set 2: {self.set2_weight} - {self.set2_reps} reps")
        if (self.set3_weight is not None) and (self.set3_reps is not None):
            valuesList.append(f"Set 3: {self.set3_weight} - {self.set3_reps} reps")
        if (self.set4_weight is not None) and (self.set4_reps is not None):
            valuesList.append(f"Set 4: {self.set4_weight} - {self.set4_reps} reps")
        if (self.set5_weight is not None) and (self.set5_reps is not None):
            valuesList.append(f"Set 5: {self.set5_weight} - {self.set5_reps} reps")
        if self.notes is not None:
            valuesList.append(f"Notes: {self.notes}")
        return valuesList

@app.get("/most_recent_workouts")
def get_recent_workouts(exercise, num_workouts):
    query = "SELECT * FROM workout_records WHERE exercise = :exercise ORDER BY date DESC LIMIT :num_workouts"
    with engine.connect() as connection:
        result = connection.execute(
            text(query),
            {"exercise": exercise, "num_workouts": num_workouts}
        )
        rows = [Workout(**row._mapping) for row in result]
    return [workout.valueswithlabels() for workout in rows]


@app.get("/workouts")
def get_workouts():
    with engine.connect() as connection:
        result = connection.execute(text("select * FROM workout_records ORDER BY date DESC"))
        rows = [Workout(**row._mapping) for row in result]
    return [workout.valueswithlabels() for workout in rows]