import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class TestLogin:
    @pytest.mark.usefixtures("setup", "test_data")
    def test_valid_login(self, test_data):
        # Get the absolute path to the HTML file
        html_path = os.path.abspath("index_mysql.html")
        self.driver.get(f"file://{html_path}")
        
        # Wait for the login form to be visible
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "loginForm"))
        )
        
        # Fill login form
        username = self.driver.find_element(By.ID, "login-username")
        password = self.driver.find_element(By.ID, "login-password")
        
        username.send_keys(test_data['valid_user']['username'])
        password.send_keys(test_data['valid_user']['password'])
        
        # Submit form
        login_button = self.driver.find_element(By.CSS_SELECTOR, "#loginForm button.auth-btn")
        login_button.click()
        
        # Wait for user info to appear
        user_info = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".user-info .customFontForDescriptiveH4 span"))
        )
        assert test_data['valid_user']['username'] in user_info.text

        # Perform logout
        logout_button = self.driver.find_element(By.CSS_SELECTOR, "button.customLogoutBtn")
        logout_button.click()
        
        # Wait for auth container to reappear
        auth_container = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "auth-container"))
        )
        assert auth_container.is_displayed()

    @pytest.mark.usefixtures("setup", "test_data")
    def test_invalid_login(self, test_data):
        # Get the absolute path to the HTML file
        html_path = os.path.abspath("index_mysql.html")
        self.driver.get(f"file://{html_path}")
        
        # Wait for the login form to be visible
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "loginForm"))
        )
        
        # Fill login form
        username = self.driver.find_element(By.ID, "login-username")
        password = self.driver.find_element(By.ID, "login-password")
        
        username.send_keys(test_data['invalid_user']['username'])
        password.send_keys(test_data['invalid_user']['password'])
        
        # Submit form
        login_button = self.driver.find_element(By.CSS_SELECTOR, "#loginForm button.auth-btn")
        login_button.click()
        
        # Wait for error message
        error_msg = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.registration-message.show.error"))
        )
        assert "Invalid username or password" in error_msg.text
