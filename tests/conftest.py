import pytest
from tasks.pet_tasks import PetTasks


@pytest.fixture(scope="function")
def pet_tasks_init(mocker):
    mock_parent = mocker.MagicMock()
    instance = PetTasks(mock_parent)
    instance.req = mocker.MagicMock()
    return instance

@pytest.fixture(scope="function")
def task_instance(mocker):
    mock_parent = mocker.MagicMock()
    mock_client = mocker.MagicMock()
    mock_parent.client = mock_client
    instance = PetTasks(mock_parent)
    return instance
