import pytest
import responses

@pytest.fixture
def mock_authentication():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as res:
        res=responses.add(
            method=responses.GET,
            url='http://127.0.0.1:7000/getUser?user_id=1',
            json={"message":"User data fetched successfully",
                  "status":200, 
                  'data': {
                    'id':1,
                    'username':'Joshik',
                    'password':'@Joshi2002',
                    'email':'joshik2222@gmail.com',
                    'is_superuser':True,
                    'is_verified':'True'
            }},
        status=200,
        )
        return res
    

@pytest.fixture
def add_cart():
    return {
    "book_id": 1,
    "quantity": 2
}