import pytest

@pytest.fixture
def super_user():
    return {
    "username": "john_cena",
    "password" : "@Joshi2002",
    "email": "johncena@example.com",
    "superkey": "54321"
}
    
@pytest.fixture
def notsuper_user():
    return {
    "username": "john_notdoe",
    "password" : "@Joshi2002",
    "email": "johnnotdoe@example.com",
}
    
@pytest.fixture
def wrong_super_user():
    return {
    "username": "john_notdoe",
    "password" : "@Joshi2002",
    "email": "johnnotdoe@example.com",
    "superkey": "12345"
}
    
@pytest.fixture
def existing_user():
    return {
    "username": "john_doe",
    "password" : "@Joshi2002",
    "email": "johnnotdoe@example.com",
    "superkey": "12345"
}
    
@pytest.mark.register
def test_register(user_client,super_user):
    response = user_client.post('/users',json=super_user, headers={"Content-Type":"application/json"})
    print(response.json)
    assert response.status_code == 201

@pytest.mark.notsuperuser_register
def test_register_not_superuser(user_client,notsuper_user):
    response = user_client.post('/users',json=notsuper_user, headers={"Content-Type":"application/json"})
    print(response.json)
    assert response.status_code == 201

@pytest.mark.invalid_superuser_register
def test_register_invalid_superuser(user_client,wrong_super_user):
    response = user_client.post('/users',json=wrong_super_user, headers={"Content-Type":"application/json"})
    assert response.status_code == 400

@pytest.mark.existing_user_register
def existing_user_register(user_client,existing_user):
    response = user_client.post('/users',json=existing_user, headers={"Content-Type":"application/json"})
    assert response.status_code == 201
