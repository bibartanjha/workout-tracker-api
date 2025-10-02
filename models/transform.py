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
    warmup = None
    if row.get("warmup_weight") is not None and row.get("warmup_reps") is not None:
        warmup = ExerciseSet(weight=row["warmup_weight"], reps=row["warmup_reps"])

    return Workout(
        exercise=row["exercise"],
        date=row["date"],
        category=row.get("category"),
        warmup=warmup,
        sets=extract_sets(row),
        notes=row.get("notes"),
    )


def workout_to_db_row(workout: Workout) -> Dict[str, any]:
    row = {
        "exercise": workout.exercise,
        "date": workout.date,
        "category": workout.category,
        "notes": workout.notes,
        "warmup_weight": workout.warmup.weight if workout.warmup else None,
        "warmup_reps": workout.warmup.reps if workout.warmup else None,
    }

    for i, s in enumerate(workout.sets, start=1):
        row[f"set{i}_weight"] = s.weight
        row[f"set{i}_reps"] = s.reps

    return row
