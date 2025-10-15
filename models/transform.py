from typing import Dict, List
from sqlalchemy import inspect

from models.workout import ExerciseSet, Workout
from models.workoutplanday import WorkoutPlanDay


def extract_sets(row: Dict[str, any]) -> List[ExerciseSet]:
    sets = []
    i = 1
    while f"set{i}_weight" in row and f"set{i}_reps" in row:
        weight, reps = row.get(f"set{i}_weight"), row.get(f"set{i}_reps")
        if weight is not None and reps is not None:
            sets.append(ExerciseSet(weight=weight, reps=reps))
        i += 1
    return sets


def db_row_to_workout(row: Dict[str, any]) -> Workout:
    sets = extract_sets(row)

    return Workout(
        exercise=row["exercise"],
        date=row["date"],
        sets=sets,
        notes=row.get("notes"),
    )


def workout_to_db_row(workout: Workout) -> Dict[str, any]:
    row = {
        "exercise": workout.exercise,
        "date": workout.date,
        "notes": workout.notes if workout.notes else None
    }

    for i, s in enumerate(workout.sets, start=1):
        if (s.weight is not None) and (s.reps is not None):
            row[f"set{i}_weight"] = s.weight
            row[f"set{i}_reps"] = s.reps

    return row

def row_to_dict(row):
    return {c.key: getattr(row, c.key) for c in inspect(row).mapper.column_attrs}


def workout_plan_day_to_db_row(workout_plan_day: WorkoutPlanDay) -> Dict[str, any]:
    row = {
        "exercise": workout_plan_day.exercise,
        "day_number": workout_plan_day.day_number,
        "plan_day_description": workout_plan_day.plan_day_description,
        "date_completed": workout_plan_day.date_completed if workout_plan_day.date_completed else None
    }
    return row

def db_row_to_workout_plan_day(row: Dict[str, any]) -> WorkoutPlanDay:
    return WorkoutPlanDay(
        exercise=row["exercise"],
        day_number=row["day_number"],
        plan_day_description=row["plan_day_description"],
        date_completed=row["date_completed"]
    )
