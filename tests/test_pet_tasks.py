from urllib.error import URLError

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

test_data = [({"Item1": "1"}),
             ({"Item2": "2"}),
             ({"Item3": "3"})]
@pytest.mark.parametrize("content_value", test_data)
def test_get_pet_store_inventory_statuses_positive(pet_tasks_init, caplog, content_value):
    pet_tasks_init.req.get_request.return_value = 200, content_value
    with caplog.at_level("INFO", logger="tasks.pet_tasks"):
        pet_tasks_init.get_pet_store_inventory_statuses()
    for status, count in content_value.items():
        assert f"Status: {status}, Count: {count}" in caplog.text
    pet_tasks_init.req.get_request.assert_called_once()

test_data = [({"Item1": "1"}, False),
             ({"Item2": "2"}, None),
             ({"Item3": "3"}, False)]
@pytest.mark.parametrize("content_value, status_code_value", test_data)
def test_get_pet_store_inventory_statuses_negative(pet_tasks_init, caplog, content_value, status_code_value):
    pet_tasks_init.req.get_request.return_value = status_code_value, content_value
    with caplog.at_level("ERROR", logger="tasks.pet_tasks"):
        pet_tasks_init.get_pet_store_inventory_statuses()
    assert "Failed to get pet store inventory for request." in caplog.text
    pet_tasks_init.req.get_request.assert_called_once()

def test_place_an_order_for_a_pet_positive(pet_tasks_init, caplog):
    pet_tasks_init.req.post_request.return_value = True
    with caplog.at_level("INFO"):
        pet_tasks_init.place_an_order_for_a_pet()

    assert "Order for purchasing the pet success."
    pet_tasks_init.req.post_request.assert_called_once()

def test_place_an_order_for_a_pet_negative(pet_tasks_init, caplog):
    pet_tasks_init.req.post_request.return_value = False
    with caplog.at_level("INFO"):
        pet_tasks_init.place_an_order_for_a_pet()

    assert "Order for purchasing the pet fail."
    pet_tasks_init.req.post_request.assert_called_once()

test_data = [({"id": 1, "firstName": "Adam"}),
             {"id": 1, "firstName": "Kevin"},
             {"id": 1, "firstName": "Michael"}]
@pytest.mark.parametrize("payload_data_value", test_data)
def test_update_first_user_data_positive(pet_tasks_init, caplog, payload_data_value):
    pet_tasks_init.all_pets_payload_data = payload_data_value
    pet_tasks_init.req.post_request.return_value = True
    with caplog.at_level("INFO"):
        pet_tasks_init.update_first_user_data()
    assert "Start updating user data." in caplog.text
    assert f"User with id {payload_data_value["id"]} modified successfully." in caplog.text

test_data = [None,
             {"id": 1, "firstName": "Kevin"},
             {"id": 1, "firstName": "Michael"}]
@pytest.mark.parametrize("payload_data_value", test_data)
def test_update_first_user_data_negative(pet_tasks_init, caplog, payload_data_value):
    pet_tasks_init.all_pets_payload_data = [payload_data_value] if payload_data_value else []
    pet_tasks_init.req.put_request.return_value = False
    with caplog.at_level("ERROR"):
        pet_tasks_init.update_first_user_data()
    if payload_data_value:
        expected_log = f"Failed to modify user with id: {payload_data_value['id']}."
        assert expected_log in caplog.text
    else:
        assert f"Failed to modify user" in caplog.text

test_data = [({"id": 1, "firstName": "Adam"}, {"id": 2, "firstName": "Michael"}),
             ({"id": 5, "firstName": "Adam"}, {"id": 3, "firstName": "Jan"}),
             ({"id": 10, "firstName": "Adam"}, {"id": 4, "firstName": "Sandra"})]
@pytest.mark.parametrize("payload_value", test_data)
def test_delete_non_existing_pet_positive(pet_tasks_init, payload_value):
    pet_tasks_init.all_pets_payload_data = payload_value
    pet_tasks_init.req.delete_request_expect_error_404.return_value = True
    pet_tasks_init.delete_non_existing_pet()
    pet_tasks_init.req.delete_request_expect_error_404.assert_called_once()

test_data = [None,
             ({"id": 5, "firstName": "Adam"}, {"id": 3, "firstName": "Jan"}),
             ({"id": 10, "firstName": "Adam"}, {"id": 4, "firstName": "Sandra"})]
@pytest.mark.parametrize("payload_value", test_data)
def test_delete_non_existing_pet_negative(pet_tasks_init, payload_value):
    pet_tasks_init.all_pets_payload_data = list(payload_value) if payload_value else []
    pet_tasks_init.req.delete_request_expect_error_404.side_effect = URLError(reason="Error")
    with pytest.raises(URLError):
        pet_tasks_init.delete_non_existing_pet()
    pet_tasks_init.req.delete_request_expect_error_404.assert_called_once()