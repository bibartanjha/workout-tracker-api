from sqlalchemy.dialects.mysql import SMALLINT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Date, String, Integer, Text, NUMERIC, Boolean

from database import Base

class ExerciseCategoryRecord(Base):
    __tablename__ = "v1a_push_pull_legs"
    __table_args__ = {"schema": "split_days"}

    exercise = Column(String, primary_key=True, unique=True, nullable=False)
    split_category = Column(String, nullable=False)


class WorkoutRecord(Base):
    __tablename__ = "v1a_weight_lifting_records"
    __table_args__ = {"schema": "exercise_records"}

    id = Column(UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()")
    date = Column(Date)
    exercise = Column(Text)
    notes = Column(Text, nullable=True)

    set1_weight = Column(NUMERIC, nullable=True)
    set1_reps = Column(Integer, nullable=True)
    set2_weight = Column(NUMERIC, nullable=True)
    set2_reps = Column(Integer, nullable=True)
    set3_weight = Column(NUMERIC, nullable=True)
    set3_reps = Column(Integer, nullable=True)
    set4_weight = Column(NUMERIC, nullable=True)
    set4_reps = Column(Integer, nullable=True)
    set5_weight = Column(NUMERIC, nullable=True)
    set5_reps = Column(Integer, nullable=True)


class WorkoutPlanRecord(Base):
    __tablename__ = "v1a_workout_plans"
    __table_args__ = {"schema": "workout_plans"}

    id = Column(UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()")
    exercise = Column(Text)
    day_number = Column(SMALLINT)
    plan_description = Column(Text)
    completed = Column(Boolean, default=False, nullable=True)
    date_completed = Column(Date, nullable=True)



