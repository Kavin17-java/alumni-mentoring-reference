import pytest
import database


@pytest.fixture
def temporary_database(tmp_path, monkeypatch):
    path = tmp_path / "test.sqlite"
    monkeypatch.setattr(database, "DATABASE_PATH", path)
    database.initialize_database()
    yield path
