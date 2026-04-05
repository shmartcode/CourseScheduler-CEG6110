# tests/test_login.py
import sys
import os

# Add the root directory to sys.path so Python can find login.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import accounts

# NOTE FOR ALL TESTS: Each test checks if the return type is str 
# (an error message) if the criteria are not met, or if the method returns true.
def test_check_criteria_username_seven_lowercase():
    
    test_username = "student"
    correct_password = "Password123$"
    
    assert type(accounts.check_criteria(test_username, correct_password)) == str
    
def test_check_criteria_username_nine_lowercase():
    
    test_username = "expedient"
    correct_password = "Password123$"
    
    assert type(accounts.check_criteria(test_username, correct_password)) == str
    
def test_check_criteria_username_eight_lowercase():
    
    test_username = "peculiar"
    correct_password = "Password123$"
    
    assert accounts.check_criteria(test_username, correct_password) == True
    
def test_check_criteria_username_null():
    
    test_username = ""
    correct_password = "Password123$"
    
    assert type(accounts.check_criteria(test_username, correct_password)) == str
    
def test_check_criteria_username_seven_uppercase():
    
    test_username = "STUDENT"
    correct_password = "Password123$"
    
    assert type(accounts.check_criteria(test_username, correct_password)) == str
    
def test_check_criteria_username_nine_uppercase():
    
    test_username = "EXPEDIENT"
    correct_password = "Password123$"
    
    assert type(accounts.check_criteria(test_username, correct_password)) == str
    
def test_check_criteria_username_eight_uppercase():
    
    test_username = "PECULIAR"
    correct_password = "Password123$"
    
    assert type(accounts.check_criteria(test_username, correct_password)) == str
    
def test_check_criteria_password_eleven_characters():
    
    correct_username = "username"
    test_password = "Password12%"
    
    assert type(accounts.check_criteria(correct_username, test_password)) == str
    
def test_check_criteria_password_thirteen_characters():
    
    correct_username = "username"
    test_password = "Password1234%"
    
    assert type(accounts.check_criteria(correct_username, test_password)) == str

def test_check_criteria_password_twelve_characters():
    
    correct_username = "username"
    test_password = "Password123%"
    
    assert accounts.check_criteria(correct_username, test_password) == True
    
def test_check_criteria_password_null():
    
    corect_username = "username"
    test_password = ""
    
    assert type(accounts.check_criteria(corect_username, test_password)) == str
    
def test_check_criteria_password_no_uppercase():
    
    correct_username = "username"
    test_password = "password123$"
    
    assert type(accounts.check_criteria(correct_username, test_password)) == str
    
def test_check_criteria_password_no_lowercase():
    
    correct_username = "username"
    test_password = "PASSWORD123$"
    
    assert type(accounts.check_criteria(correct_username, test_password)) == str
    
def test_check_criteria_password_no_digit():
    
    correct_username = "username"
    test_password = "PasswordABC$"
    
    assert type(accounts.check_criteria(correct_username, test_password)) == str
    
def test_check_criteria_password_no_special_character():
    
    correct_username = "username"
    test_password = "Password1234"
    
    assert type(accounts.check_criteria(correct_username, test_password)) == str