import json
from typing import Any, Optional

from sqlalchemy import (
    Column,
    Computed,
    case,
    create_engine,
    delete,
    func,
    select,
    text,
    update,
)
from sqlalchemy.dialects.postgresql import Insert, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session, declarative_base, mapped_column, sessionmaker
from sqlalchemy.schema import DropTable

from fashion_hub_backend.errors import APINotFound
from fashion_hub_backend.interface.fastapi.app_config import config

SQLALCHEMY_DATABASE_URL = f"postgresql://{config.database_username}:{config.database_password}@{config.database_hostname}:{config.database_port}/{config.database_name}"
# SQLALCHEMY_DATABASE_URL="postgresql://fashion_hub:iPwl96PN8zH0JPsCr0Hn4Rbo5U6vXjhC@dpg-d10ttrje5dus73amjmrg-a.frankfurt-postgres.render.com/fashion_hub_1j7i"
# SQLALCHEMY_DATABASE_URL = (
#     f"postgresql://{config.database_username}:"
#     f"{config.database_password}@{config.database_hostname}/"
#     f"{config.database_name}"
#     f"?sslmode=require&channel_binding=require"
# )

print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(url=SQLALCHEMY_DATABASE_URL, echo=config.debug_sql_echo, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DeclarativeBase = declarative_base()


class Base(DeclarativeBase):
    """
    Base class for sqlalchemy models
    """

    __abstract__ = True

    @classmethod
    def get(cls, db: Session, ident):
        return db.get(cls, ident=ident)

    @classmethod
    def get_or_raise(cls, db: Session, ident, detail: str | None = None):
        obj = db.get(cls, ident=ident)
        if obj is None:
            raise APINotFound(key=ident, detail=detail)
        return obj

    @classmethod
    def select(cls):
        return select(cls)

    @classmethod
    def count(cls):
        return select(func.count()).select_from(cls)

    @classmethod
    def insert(cls, returning_full_model: bool = True):
        query = insert(cls)
        if returning_full_model:
            query = query.returning(cls)
        return query

    @classmethod
    def update(cls):
        return update(cls)

    @classmethod
    def delete(cls):
        return delete(cls)

    @classmethod
    def on_conflict_do_update(
        cls,
        query: Insert,
        index_elements: Optional[list[str | Column]] = None,
    ):
        """
        Turns an INSERT statement into INSERT ... ON CONFLICT UPDATE,
        i.e., an UPSERT operation.

        If no index_elements are provided, they default to the tables primary keys.
        """
        if index_elements is None:
            index_elements = inspect(cls).primary_key
        set_columns = {
            column.name: column
            for column in query.excluded
            if not (column.primary_key or column in index_elements or column.name in index_elements)
        }
        return query.on_conflict_do_update(
            index_elements=index_elements,
            set_=set_columns,
        )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def setup_db(
    db: Session,
):
    db.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    db.commit()


def reset_table(db: Session, table: type[Base]):
    try:
        db.query(table).delete()
        db.commit()
        return
    except:  # noqa: E722
        print(f"Could not delete table {table}.")
        return


def load_defaults(db: Session, table: type[Base], file_path: str, recreate: bool = False):
    with open(file_path) as fs:
        table_data = json.load(fs)

    if recreate:
        db.query(table).delete()
        db.commit()

    for row_data in table_data:
        entry = db.query(table).filter_by(**row_data).first()
        if entry is None:
            try:
                new_row = table(**row_data)
                db.add(new_row)
                db.commit()
            except IntegrityError as e:
                print(RuntimeWarning(f"Could not add row {row_data} in table {table.__name__}."))
                print(e)


# def load_default_data(db: Session):
#     from test_gpt_backend.config_llm.models import ConfigLLMTable
#     load_defaults(db, ConfigLLMTable, "./test_gpt_backend/config_llm/llm_defaults.json", True)


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


def computed_column_with_cases(db_type: type, whens: list[tuple[Any, Any]], **kwargs):
    """
    Create a computed database column with conditional logic.

    This function generates a computed column for a database table, where the value of the column
    is determined by a series of CASE statements. The column type and the conditions for the CASE
    statements are specified as parameters.

    Args:
        db_type (type): The data type of the computed column.
        whens (List[Tuple[Any, Any]]): A list of tuples where each tuple represents a condition and
                                       the corresponding value if the condition is met (in the format
                                       (condition, result)).
        **kwargs: Additional keyword arguments to be passed to mapped_column.

    Returns:
        Column: A SQLAlchemy `Column` object configured with the computed case logic.
    """
    return mapped_column(
        db_type,
        Computed(case(*whens)),
        **kwargs,
    )
