import pytest
import os
from pathlib import Path
from core.config import Config

@pytest.fixture(scope="session")
def test_config():
    # Set environment to testing
    os.environ['APP_ENV'] = 'testing'
    
    # Create temporary config directory
    base_dir = Path(__file__).resolve().parent.parent
    config_path = base_dir / 'config'
    
    # Load test config
    config = Config()
    yield config
    
    # Cleanup
    del os.environ['APP_ENV']