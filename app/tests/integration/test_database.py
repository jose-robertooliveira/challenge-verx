from app.database import engine


def test_database_connection() -> None:
    assert engine is not None
