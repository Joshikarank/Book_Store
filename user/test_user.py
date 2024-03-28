import pytest

@pytest.fixture
def super_user():
    return {
        "username" : "Felixkaran",
        "email" : "felixjk22@gmail.com",
        "password" : "@Felixkaran2002",
        "superkey" : "54321"
        }
    
# @pytest.mark.register
def test_register(user_client,super_user):
    response = user_client.post('/users',json=super_user, headers={"Content-Type":"application/json"})
    assert response.status_code == 201
    