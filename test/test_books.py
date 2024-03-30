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
def book_add_data():
    return {
    "title": "A Title of a Books",
    "author": "A random Author",
    "price": 106.0,
    "quantity": 2
}
    
@pytest.fixture
def invalid_book():
    return {
    "title": "A Title of a Books",
    "author": "A random Author",
    "price": "",
    "quantity": 0
}


@pytest.mark.get_book
@responses.activate
def test_get_book_data(book_client,token, mock_authentication):
    book_data =  {
    "title": "A Title of a Books",
    "author": "A random Author",
    "price": 106.0,
    "quantity": 2
    }
    
    response = book_client.post('/addbook',json=book_data, headers={"Content-type":"application/json","Authorization": token})
    
    get_book = book_client.get('/getbook', headers={"Content-type":"application/json","Authorization": token})
    
    print(get_book.json)
    assert get_book.status_code == 200
    

@pytest.mark.delete_book
@responses.activate
def test_delete_book_data(book_client,token, mock_authentication):
    book_data =  {
    "title": "A random Title of a Books",
    "author": "A random Author",
    "price": 106.0,
    "quantity": 2
    }
    response = book_client.post('/addbook',json=book_data, headers={"Content-type":"application/json","Authorization": token})
    del_book = book_client.delete('/deletebook?book_id=1', headers={"Content-type":"application/json","Authorization": token})
    assert del_book.status_code == 204


@pytest.mark.updatebooks
@responses.activate
def test_updatebooks_data(book_client,token, mock_authentication):
    book_data1 =  {
    "title": "Arandom Title of a Books",
    "author": "Arandom Author",
    "price": 106.0,
    "quantity": 2
    }
    response = book_client.post('/addbook',json=book_data1, headers={"Content-type":"application/json","Authorization": token})
    updates =  {
    "title": "Arandom Title of a Books",
    "author": "An Author",
    "price": 100.0,
    "quantity": 20
    }
    update_response = book_client.put('/updatebooks?book_id=1',json=updates, headers={"Content-type":"application/json","Authorization": token})
    assert update_response.status_code == 200



@pytest.mark.addbook
@responses.activate
def test_add_book(book_client,book_add_data,token, mock_authentication):
    response = book_client.post('/addbook',json=book_add_data, headers={"Content-type":"application/json",
                                                                             "Authorization": token})
    print(response.json)
    assert response.status_code == 201

@pytest.mark.invalid_book
@responses.activate
def test_invalid_book(book_client,invalid_book,token, mock_authentication):
    response = book_client.post('/addbook',json=invalid_book, headers={"Content-type":"application/json",
                                                                             "Authorization": token})
    print(response.json)
    assert response.status_code == 400


@pytest.mark.invalid_book_token
@responses.activate
def test_invalid_book_token(book_client,book_add_data):
    response = book_client.post('/addbook',json=book_add_data, headers={"Content-type":"application/json"})
    print(response.json)
    assert response.status_code == 404