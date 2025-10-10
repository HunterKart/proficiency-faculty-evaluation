"""Integration test to ensure Alembic migrations apply cleanly."""

from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Set

import sqlalchemy as sa
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

from src.models.academic import Department, Program
from src.models.identity import University

HEAD_REVISION = "e7bc8b1da6f7"


@contextmanager
def _override_database_url(url: str):
    """Temporarily set DATABASE_URL for Alembic execution."""

    previous_url: Optional[str] = os.environ.get("DATABASE_URL")
    os.environ["DATABASE_URL"] = url
    try:
        yield
    finally:
        if previous_url is not None:
            os.environ["DATABASE_URL"] = previous_url
        else:
            os.environ.pop("DATABASE_URL", None)


def test_initial_migration_executes(tmp_path) -> None:
    """Applying the head migration should create core tables and relationships."""

    base_dir = Path(__file__).resolve().parents[2]
    alembic_cfg = Config(str(base_dir / "alembic.ini"))
    alembic_cfg.set_main_option("script_location", str(base_dir / "alembic"))

    db_url = f"sqlite:///{tmp_path / 'migration.db'}"
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)

    with _override_database_url(db_url):
        command.upgrade(alembic_cfg, "head")
        # Idempotency: second run should be a no-op
        command.upgrade(alembic_cfg, "head")

    engine = create_engine(db_url, future=True)

    try:
        inspector = inspect(engine)

        with engine.connect() as connection:
            version = connection.execute(
                sa.text("SELECT version_num FROM alembic_version")
            ).scalar_one()
        assert version == HEAD_REVISION

        tables: Set[str] = set(inspector.get_table_names())
        assert {"universities", "departments", "programs", "users"}.issubset(tables)

        program_columns = {column["name"] for column in inspector.get_columns("programs")}
        assert {
            "id",
            "university_id",
            "department_id",
            "name",
            "program_code",
            "created_at",
            "updated_at",
        }.issubset(program_columns)

        unique_constraints = {
            constraint["name"]
            for constraint in inspector.get_unique_constraints("programs")
            if constraint.get("name")
        }
        assert "uk_university_program_code" in unique_constraints

        program_fk_targets = {
            fk["referred_table"] for fk in inspector.get_foreign_keys("programs")
        }
        assert {"universities", "departments"} <= program_fk_targets

        with Session(engine) as session:
            university = University(name="QA University")
            department = Department(name="College of Engineering", university=university)
            program = Program(
                name="BS Computer Engineering",
                program_code="BS-CE",
                university=university,
                department=department,
            )

            session.add(program)
            session.commit()

            session.refresh(program)
            assert program.department is department
            assert program.university is university

            reloaded_university = session.get(University, university.id)
            assert reloaded_university is not None
            assert reloaded_university.departments[0].programs[0].program_code == "BS-CE"
    finally:
        engine.dispose()
