import pytest
from tasks.pet_tasks import PetTasks
from typing import Any


@pytest.fixture(scope="function")
def pet_tasks_init(mocker: Any) -> PetTasks:
    """
    Pytest fixture that creates a mocked PetTasks instance.
    
    Creates a PetTasks instance with a mocked parent and request handler,
    suitable for unit testing without actual HTTP calls.
    
    Args:
        mocker: Pytest-mock mocker fixture for creating mock objects.
        
    Returns:
        PetTasks: A PetTasks instance with mocked dependencies.
    """
    mock_parent = mocker.MagicMock()
    instance = PetTasks(mock_parent)
    instance.req = mocker.MagicMock()
    return instance

@pytest.fixture(scope="function")
def task_instance(mocker: Any) -> PetTasks:
    """
    Pytest fixture that creates a PetTasks instance with a mocked client.
    
    Creates a PetTasks instance where the parent's client is mocked,
    allowing testing of client interactions.
    
    Args:
        mocker: Pytest-mock mocker fixture for creating mock objects.
        
    Returns:
        PetTasks: A PetTasks instance with mocked client.
    """
    mock_parent = mocker.MagicMock()
    mock_client = mocker.MagicMock()
    mock_parent.client = mock_client
    instance = PetTasks(mock_parent)
    return instance
