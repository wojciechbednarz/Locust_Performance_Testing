import pytest
from locust.exception import ResponseError

test_data = ["Pet1", "Pet2", "Pet3"]
@pytest.mark.parametrize("fake_name", test_data)
def test_create_pet_positive(pet_tasks_init, caplog, mocker, fake_name):
    mocker.patch("tasks.pet_tasks.create_pet_fake_name", return_value=fake_name)
    pet_tasks_init.req.post_request.return_value = True
    with caplog.at_level("INFO"):
        pet_tasks_init.create_pet()

    assert f"Pet with name {fake_name} created successfully."
    pet_tasks_init.req.post_request.assert_called_once()

test_data = ["Pet1", "Pet2", "Pet3"]
@pytest.mark.parametrize("fake_name", test_data)
def test_create_pet_negative(pet_tasks_init, caplog, mocker, fake_name):
    mocker.patch("tasks.pet_tasks.create_pet_fake_name", return_value=fake_name)
    pet_tasks_init.req.post_request.side_effect = ResponseError
    with pytest.raises(ResponseError):
        pet_tasks_init.create_pet()
        assert f"Failed to create pet: {fake_name}"
        pet_tasks_init.req.post_request.assert_called_once()

test_data = ["User1", "User2", "User3"]
@pytest.mark.parametrize("fake_name", test_data)
def test_create_user_positive(pet_tasks_init, caplog, mocker, fake_name):
    mocker.patch("tasks.pet_tasks.create_fake_username", return_value=fake_name)
    pet_tasks_init.req.post_request.return_value = True
    with caplog.at_level("INFO"):
        pet_tasks_init.create_user()

    assert f"Pet with username {fake_name} created successfully."
    pet_tasks_init.req.post_request.assert_called_once()

test_data = ["User1", "User2", "User3"]
@pytest.mark.parametrize("fake_name", test_data)
def test_create_user_negative(pet_tasks_init, caplog, mocker, fake_name):
    mocker.patch("tasks.pet_tasks.create_pet_fake_name", return_value=fake_name)
    pet_tasks_init.req.post_request.side_effect = ResponseError
    with pytest.raises(ResponseError):
        pet_tasks_init.create_user()
        assert f"Failed to create user with username: {fake_name}"
        pet_tasks_init.req.post_request.assert_called_once()

def test_on_start(pet_tasks_init, mocker):
    mock_create_pet = mocker.patch.object(pet_tasks_init, "create_pet")
    mock_create_user = mocker.patch.object(pet_tasks_init, "create_user")
    pet_tasks_init.on_start()
    mock_create_pet.assert_called_once()
    mock_create_user.assert_called_once()

def test_get_main_page(task_instance):
    task_instance.get_main_page()
    task_instance.client.get.assert_called_once_with("/")

def test_get_pet_store_inventory_statuses_positive(mocker):
    pass
