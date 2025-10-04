from typing import Dict, List

from models.workout import ExerciseSet, Workout


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
