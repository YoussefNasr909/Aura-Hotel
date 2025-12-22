"""
Test cases for the Dashboard page.
Covers: authentication requirement, stats display, test results display.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def reset_session(driver, base_url):
    driver.get(base_url + "/test/reset")


def login(driver, base_url):
    driver.get(base_url + "/login")
    driver.find_element(By.CSS_SELECTOR, '[data-test="login-username"]').send_keys("admin")
    driver.find_element(By.CSS_SELECTOR, '[data-test="login-password"]').send_keys("1234")
    driver.find_element(By.CSS_SELECTOR, '[data-test="login-submit"]').click()
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="nav-logout"]'))
    )


def test_dashboard_requires_login(driver, base_url):
    """Test that dashboard redirects to login if not authenticated."""
    reset_session(driver, base_url)
    driver.get(base_url + "/dashboard")
    
    # Should redirect to login page
    WebDriverWait(driver, 5).until(EC.url_contains("/login"))
    assert "/login" in driver.current_url


def test_dashboard_shows_room_stats(driver, base_url):
    """Test that dashboard displays room count correctly."""
    reset_session(driver, base_url)
    login(driver, base_url)
    
    driver.get(base_url + "/dashboard")
    
    # Wait for dashboard to load
    rooms_stat = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="dash-rooms"]'))
    )
    
    # Should show 6 rooms (we added 3 new rooms earlier)
    assert rooms_stat.text == "6"


def test_dashboard_shows_test_automation_section(driver, base_url):
    """Test that dashboard shows test automation results section."""
    reset_session(driver, base_url)
    login(driver, base_url)
    
    driver.get(base_url + "/dashboard")
    
    # Wait for test status badge to appear
    test_status = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="test-status"]'))
    )
    
    # Status should be either PASS, FAIL, or No Runs Yet
    status_text = test_status.text.upper()
    assert "PASS" in status_text or "FAIL" in status_text or "NO RUNS" in status_text
