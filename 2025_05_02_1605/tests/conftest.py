import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

@pytest.fixture(scope="class")
def setup(request):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--start-maximized')
    
    try:
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()
        request.cls.driver = driver
        yield
        driver.quit()
    except Exception as e:
        print(f"Error starting Chrome: {e}")
        raise

@pytest.fixture(scope="class")
def test_data():
    return {
        'valid_user': {
            'username': 'testuser',
            'password': 'password123'
        },
        'invalid_user': {
            'username': 'nonexistent',
            'password': 'wrongpass'
        },
        'new_user': {
            'username': 'newuser',
            'password': 'newpassword123',
            'confirm_password': 'newpassword123'
        }
    }
