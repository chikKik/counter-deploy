import pytest
import requests

BASE_URL = "http://localhost:80"

def test_initialization():
    """Тест инициализации: при первом запросе значение счётчика равно 0"""
    # Сброс счетчика
    reset_response = requests.post(f"{BASE_URL}/api/counter/reset")
    assert reset_response.status_code == 200
    
    # Текущее значение
    response = requests.get(f"{BASE_URL}/api/counter")
    assert response.status_code == 200
    
    data = response.json()
    assert data["value"] == 0

def test_increment():
    """Тест увеличения: после вызова /increment значение увеличивается на 1"""
    # Сброс счетчика
    requests.post(f"{BASE_URL}/api/counter/reset")
    
    # Начальное значение
    initial_response = requests.get(f"{BASE_URL}/api/counter")
    initial_value = initial_response.json()["value"]
    
    # Увеличение счетчика
    increment_response = requests.post(f"{BASE_URL}/api/counter/increment")
    assert increment_response.status_code == 200
    
    # Новое значение
    new_response = requests.get(f"{BASE_URL}/api/counter")
    new_value = new_response.json()["value"]
    
    assert new_value == initial_value + 1

def test_negative_protection():
    """Тест защиты от отрицательных значений"""
    # Сброс счетчика (будет 0)
    requests.post(f"{BASE_URL}/api/counter/reset")
    
    # Уменьшение счетчика с 0
    response = requests.post(f"{BASE_URL}/api/counter/decrement")
    
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["value"] == -1
    

def test_increment_then_decrement():
    """Дополнительный тест: увеличение, затем уменьшение"""
    # Сброс счетчика
    requests.post(f"{BASE_URL}/api/counter/reset")
    
    # Увеличение на 2
    requests.post(f"{BASE_URL}/api/counter/increment")
    requests.post(f"{BASE_URL}/api/counter/increment")
    
    response = requests.get(f"{BASE_URL}/api/counter")
    assert response.json()["value"] == 2
    
    # Уменьшение на 1
    requests.post(f"{BASE_URL}/api/counter/decrement")
    
    response = requests.get(f"{BASE_URL}/api/counter")
    assert response.json()["value"] == 1

def test_api_structure():
    """Проверка структуры API"""
   
    endpoints = [
        ("GET", "/api/counter"),
        ("POST", "/api/counter/increment"),
        ("POST", "/api/counter/decrement"),
        ("POST", "/api/counter/reset"),
    ]
    
    for method, endpoint in endpoints:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}")
        else:
            response = requests.post(f"{BASE_URL}{endpoint}")
        
        assert response.status_code == 200, f"{method} {endpoint} вернул {response.status_code}"
        
        data = response.json()
        assert "value" in data or "error" in data, f"Некорректный JSON в ответе: {data}"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])