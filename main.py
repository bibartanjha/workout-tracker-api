from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import database
from models import orm
from models.orm import ExerciseCategoryRecord, WorkoutRecord
from models.transform import db_row_to_workout, workout_to_db_row
from models.workout import Workout

orm.Base.metadata.create_all(bind=database.engine)
app = FastAPI()


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error with making request to DB.",
            "path": str(request.url),
            "error": str(exc)
        }
    )

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/categories", response_model=List[str])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(ExerciseCategoryRecord.split_category).distinct().all()
    return [c[0] for c in categories]


@app.get("/exercises_in_category", response_model=List[str])
def get_exercises_in_category(split_category: str, db: Session = Depends(get_db)):
    rows = db.query(ExerciseCategoryRecord.exercise).filter(
        ExerciseCategoryRecord.split_category == split_category
    ).all()
    exercises = [row.exercise for row in rows]
    return exercises

@app.post("/add_workout", response_model=Workout)
def add_workout(workout: Workout, db: Session = Depends(get_db)):
    row_data = workout_to_db_row(workout)
    new_workout = WorkoutRecord(**row_data)

    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)

    return db_row_to_workout(row_to_dict(new_workout))

@app.get("/most_recent_workouts", response_model=List[Workout])
def get_recent_workouts(exercise: str, num_workouts: int, db: Session = Depends(get_db)):
    rows = db.query(WorkoutRecord).filter(WorkoutRecord.exercise == exercise).order_by(WorkoutRecord.date.desc()).limit(num_workouts)
    return [db_row_to_workout(row_to_dict(row)) for row in rows]

@app.post("/add_new_exercise_to_category")
def add_exercise_to_category(exercise: str, split_category: str, db: Session = Depends(get_db)):
    new_entry = ExerciseCategoryRecord(exercise=exercise, split_category=split_category)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return {"exercise": new_entry.exercise, "split_category": new_entry.split_category}


@app.get("/workouts", response_model=List[Workout])
def get_workouts(db: Session = Depends(get_db)):
    rows = db.query(WorkoutRecord).all()
    return [db_row_to_workout(row_to_dict(row)) for row in rows]


def row_to_dict(row):
    return {c.key: getattr(row, c.key) for c in inspect(row).mapper.column_attrs}


@app.get("/workouts_by_date", response_model=List[Workout])
def get_workouts_by_date(date: str, db: Session = Depends(get_db)):
    rows = db.query(WorkoutRecord).filter(WorkoutRecord.date == date).all()
    return [db_row_to_workout(row_to_dict(row)) for row in rows]