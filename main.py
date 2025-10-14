from datetime import date
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import database
from models import orm
from models.orm import ExerciseCategoryRecord, WorkoutRecord, WorkoutPlanRecord
from models.transform import db_row_to_workout, workout_to_db_row, row_to_dict, workout_plan_to_db_row, \
    db_row_to_workout_plan
from models.workout import Workout
from models.workoutplan import WorkoutPlan

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

# Exercise category endpoints:

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


@app.post("/add_new_exercise_to_category")
def add_exercise_to_category(exercise: str, split_category: str, db: Session = Depends(get_db)):
    new_entry = ExerciseCategoryRecord(exercise=exercise, split_category=split_category)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return {"exercise": new_entry.exercise, "split_category": new_entry.split_category}

# WorkoutRecord endpoints:

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

@app.get("/workouts_by_date", response_model=List[Workout])
def get_workouts_by_date(date: str, db: Session = Depends(get_db)):
    rows = db.query(WorkoutRecord).filter(WorkoutRecord.date == date).all()
    return [db_row_to_workout(row_to_dict(row)) for row in rows]


# WorkoutPlan endpoints:

@app.post("/add_workout_plan", response_model=WorkoutPlan)
def add_workout_plan(exercise: str, day_number: int, plan_description: str, db: Session = Depends(get_db)):
    new_plan = WorkoutPlan(exercise=exercise, day_number=day_number, plan_description=plan_description)
    row_data = workout_plan_to_db_row(new_plan)
    new_workout_plan = WorkoutPlanRecord(**row_data)

    db.add(new_workout_plan)
    db.commit()
    db.refresh(new_workout_plan)

    return db_row_to_workout_plan(row_to_dict(new_workout_plan))


@app.post("/set_workout_plan_as_complete", response_model=WorkoutPlan)
def set_workout_plan_as_complete(exercise: str, day_number: int, date_completed: date, db: Session = Depends(get_db)):
    workout_plan = (
        db.query(WorkoutPlanRecord)
        .filter(
            WorkoutPlanRecord.exercise == exercise,
            WorkoutPlanRecord.day_number == day_number
        )
        .first()
    )

    if not workout_plan:
        raise HTTPException(status_code=404, detail="Workout plan not found in DB")

    workout_plan.date_completed = date_completed
    db.commit()
    db.refresh(workout_plan)

    return db_row_to_workout_plan(row_to_dict(workout_plan))

@app.get("/get_workout_plans", response_model=List[WorkoutPlan])
def get_workout_plans(exercise: str, db: Session = Depends(get_db)):
    workout_plans = (
        db.query(WorkoutPlanRecord)
        .filter(WorkoutPlanRecord.exercise == exercise)
        .order_by(WorkoutPlanRecord.day_number)
        .all()
    )

    return [db_row_to_workout_plan(row_to_dict(workout_plan)) for workout_plan in workout_plans]

@app.get("/get_all_exercises_with_plans", response_model=List[str])
def get_all_exercises_with_plans(db: Session = Depends(get_db)):
    exercises = db.query(WorkoutPlanRecord.exercise).distinct().all()
    return [e[0] for e in exercises]
