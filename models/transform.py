from typing import Dict, List
from sqlalchemy import inspect

from models.workout import ExerciseSet, Workout
from models.workoutplan import WorkoutPlan


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


def workout_plan_to_db_row(workout_plan: WorkoutPlan) -> Dict[str, any]:
    row = {
        "exercise": workout_plan.exercise,
        "day_number": workout_plan.day_number,
        "completed": workout_plan.completed if workout_plan.completed else False,
        "date_completed": workout_plan.date_completed if workout_plan.date_completed else None
    }
    return row

def db_row_to_workout_plan(row: Dict[str, any]) -> WorkoutPlan:
    return WorkoutPlan(
        exercise=row["exercise"],
        day_number=row["day_number"],
        completed=row["completed"],
        date_completed=row["date_completed"]
    )
