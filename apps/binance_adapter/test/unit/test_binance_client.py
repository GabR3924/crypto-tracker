import pytest
from unittest.mock import patch, MagicMock
import sys
import os
# Añadir la raíz del proyecto al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

# Ahora puedes importar
from apps.binance_adapter import BinanceP2PClient

@pytest.fixture
def client():
    return BinanceP2PClient()

@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.status_code = 200
    mock.json.return_value = {
        "data": [
            {
                "adv": {
                    "advNo": "123456",
                    "price": "40.5",
                    "minSingleTransAmount": "350.0",
                    "maxSingleTransAmount": "5000.0",
                    "tradeMethods": [{"payType": "Banesco"}]
                },
                "advertiser": {
                    "userGrade": 2,
                    "nickName": "TestUser"
                }
            }
        ]
    }
    return mock

@patch('apps.binance_adapter.binance_client.requests.post')
def test_fetch_advertisements_valid_response(mock_post, client, mock_response):
    # Configura el mock para devolver datos simulados
    mock_post.return_value = mock_response
    
    # Ejecuta la función
    result = client.fetch_advertisements("BUY")
    
    # Verifica los resultados
    assert len(result) == 1
    assert result[0] == 40.5
    assert mock_post.called

@patch('apps.binance_adapter.binance_client.requests.post')
def test_fetch_advertisements_empty_data(mock_post, client):
    # Configura el mock para devolver una respuesta vacía
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    mock_post.return_value = mock_response
    
    # Ejecuta la función
    result = client.fetch_advertisements("BUY")
    
    # Verifica los resultados
    assert result == []
    assert mock_post.called

@patch('apps.binance_adapter.binance_client.requests.post')
def test_fetch_advertisements_http_error(mock_post, client):
    # Configura el mock para simular un error
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_post.return_value = mock_response
    
    # Ejecuta la función
    result = client.fetch_advertisements("BUY")
    
    # Verifica los resultados
    assert result == []
    assert mock_post.called

def test_process_advertisement_valid_ad(client):
    # Crea un anuncio de prueba
    ad = {
        "adv": {
            "advNo": "123456",
            "price": "40.5",
            "minSingleTransAmount": "350.0",
            "maxSingleTransAmount": "5000.0",
            "tradeMethods": [{"payType": "Banesco"}]
        },
        "advertiser": {
            "userGrade": 2,
            "nickName": "TestUser"
        }
    }
    
    # Ejecuta la función
    price, min_t, max_t = client._process_advertisement(ad, float('inf'), float('-inf'))
    
    # Verifica los resultados
    assert price == 40.5
    assert min_t == 350.0
    assert max_t == 5000.0

def test_process_advertisement_invalid_payment(client):
    # Crea un anuncio sin método de pago requerido
    ad = {
        "adv": {
            "advNo": "123456",
            "price": "40.5",
            "minSingleTransAmount": "350.0",
            "maxSingleTransAmount": "5000.0",
            "tradeMethods": [{"payType": "OtroMetodo"}]
        },
        "advertiser": {
            "userGrade": 2,
            "nickName": "TestUser"
        }
    }
    
    # Ejecuta la función
    price, min_t, max_t = client._process_advertisement(ad, float('inf'), float('-inf'))
    
    # Verifica los resultados
    assert price is None
    assert min_t == 350.0
    assert max_t == 5000.0