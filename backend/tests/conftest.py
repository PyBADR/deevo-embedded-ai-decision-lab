import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.dependencies import verify_api_key
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture
def db_session():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


async def mock_verify_api_key():
    """Mock API key verification for tests."""
    return "test-api-key"


@pytest.fixture
def override_get_db(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    # Override both database and API key verification
    app.dependency_overrides[get_db] = _override_get_db
    app.dependency_overrides[verify_api_key] = mock_verify_api_key
    yield
    app.dependency_overrides.clear()
