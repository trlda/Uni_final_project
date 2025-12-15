import pytest

@pytest.mark.django_db
def test_get_balance_eth(api_client):
    response = api_client.get('/balance/?symbol=ETH&address=0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045', format='json')
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_balance_sol(api_client):
    response = api_client.get('/balance/?symbol=SOL&address=9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM', format='json')
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_balance_btc(api_client):
    response = api_client.get('/balance/?symbol=BTC&address=1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', format='json')
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_balance_without_address(api_client):
    response = api_client.get('/balance/?symbol=BTC&address=', format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_get_balance_without_symbol(api_client):
    response = api_client.get('/balance/?symbol=&address=1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', format='json')
    assert response.status_code == 400

def test_get_balance_with_incorrect_address(api_client):
    response = api_client.get('/balance/?symbol=BTC&address=1A1zP1eP5QGefi2DMPTfTmv7DivfNa', format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_get_price(api_client, crypto_symbols):
    for symbol in crypto_symbols:
        response = api_client.get(f"/prices/?symbol={symbol}")
        assert response.status_code == 200

@pytest.mark.django_db
def test_get_price_with_incorect_symbol(api_client):
    response = api_client.get(f"/prices/?symbol=AAAA")
    assert response.status_code == 404

