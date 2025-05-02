import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class TestRegistration:
    @pytest.mark.usefixtures("setup", "test_data")
    def test_successful_registration(self, test_data):
        # Get the absolute path to the HTML file
        html_path = os.path.abspath("index_mysql.html")
        self.driver.get(f"file://{html_path}")
        
        # Wait for the registration form to be visible
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "registrationForm"))
        )
        
        # Fill registration form
        username = self.driver.find_element(By.ID, "username")
        password = self.driver.find_element(By.ID, "password")
        confirm_password = self.driver.find_element(By.ID, "confirm_password")
        
        username.send_keys(test_data['new_user']['username'])
        password.send_keys(test_data['new_user']['password'])
        confirm_password.send_keys(test_data['new_user']['confirm_password'])
        
        # Submit form
        register_button = self.driver.find_element(By.CSS_SELECTOR, "#registrationForm button.auth-btn")
        register_button.click()
        
        # Wait for login form to appear
        try:
            login_form = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "loginForm"))
            )
            assert login_form.is_displayed()
        except:
            # If login form not found, check for error message
            error_msg = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.registration-message"))
            )
            assert "Username is not unique" in error_msg.text

    @pytest.mark.usefixtures("setup", "test_data")
    def test_duplicate_username_registration(self, test_data):
        # Get the absolute path to the HTML file
        html_path = os.path.abspath("index_mysql.html")
        self.driver.get(f"file://{html_path}")
        
        # Wait for the registration form to be visible
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "registrationForm"))
        )
        
        # Fill registration form with existing username
        username = self.driver.find_element(By.ID, "username")
        password = self.driver.find_element(By.ID, "password")
        confirm_password = self.driver.find_element(By.ID, "confirm_password")
        
        username.send_keys(test_data['valid_user']['username'])
        password.send_keys(test_data['valid_user']['password'])
        confirm_password.send_keys(test_data['valid_user']['password'])
        
        # Submit form
        register_button = self.driver.find_element(By.CSS_SELECTOR, "#registrationForm button.auth-btn")
        register_button.click()
        
        # Wait for error message
        error_msg = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.registration-message"))
        )
        assert "Username is not unique" in error_msg.text
