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
def already_existing_user():
    return {
    "username": "john_doe",
    "password" : "@Joshi2002",
    "email": "johndoe@example.com",
    "superkey": "12345"
}
 
@pytest.fixture
def invalid_username():
    return {
    "username": "jo",
    "password" : "@Joshi2002",
    "email": "jonhnotdoe@example.com",
}
 
@pytest.fixture
def invalid_password():
    return {
    "username": "John_Doesnt",
    "password" : "oshi",
    "email": "jonhdoesnt@example.com",
}
 
@pytest.fixture
def invalid_password():
    return {
    "username": "John_Doesnt",
    "password" : "@Joshi2002",
    "email": "jonhdoesntexample.com",
}

@pytest.fixture
def missing_email():
    return {
    "username": "john_cena",
    "password" : "@Joshi2002",
    "superkey": "54321"
}
    
@pytest.mark.missing_email
def test_missing_email(user_client,missing_email):
    response = user_client.post('/users',json=missing_email, headers={"Content-Type":"application/json"})
    assert response.status_code == 400

@pytest.fixture
def missing_username():
    return {
    "password" : "@Joshi2002",
    "email": "johncena@example.com",
    "superkey": "54321"
}
    
@pytest.mark.missing_username
def test_missing_username(user_client,missing_username):
    response = user_client.post('/users',json=missing_username, headers={"Content-Type":"application/json"})
    assert response.status_code == 400

@pytest.fixture
def missing_password():
    return {
    "username": "john_cena",
    "email": "johncena@example.com",
    "superkey": "54321"
}
    
@pytest.mark.missing_password
def test_missing_password(user_client,missing_password):
    response = user_client.post('/users',json=missing_password, headers={"Content-Type":"application/json"})
    assert response.status_code == 400

@pytest.mark.register
def test_register(user_client,super_user):
    response = user_client.post('/users',json=super_user, headers={"Content-Type":"application/json"})
    assert response.status_code == 201

@pytest.mark.notsuperuser_register
def test_register_not_superuser(user_client,notsuper_user):
    response = user_client.post('/users',json=notsuper_user, headers={"Content-Type":"application/json"})
    assert response.status_code == 201



@pytest.mark.invalid_superuser_register
def test_register_invalid_superuser(user_client,wrong_super_user):
    response = user_client.post('/users',json=wrong_super_user, headers={"Content-Type":"application/json"})
    assert response.status_code == 400

@pytest.mark.test_existing_user_register
def test_existing_user_register(user_client,already_existing_user):
    response = user_client.post('/users',json=already_existing_user, headers={"Content-Type":"application/json"})
    assert response.status_code == 400

@pytest.mark.test_invalid_username_register
def test_inavild_username_register(user_client,invalid_username):
    response = user_client.post('/users',json=invalid_username, headers={"Content-Type":"application/json"})
    assert response.status_code == 400

@pytest.mark.test_invalid_password_register
def test_inavild_password_register(user_client,invalid_username):
    response = user_client.post('/users',json=invalid_username, headers={"Content-Type":"application/json"})
    assert response.status_code == 400

@pytest.mark.test_invalid_email_register
def test_inavild_email_register(user_client,invalid_username):
    response = user_client.post('/users',json=invalid_username, headers={"Content-Type":"application/json"})
    assert response.status_code == 400

