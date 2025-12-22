from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


def test_rooms_search_suite_found(driver, base_url):
    driver.get(base_url + "/rooms?q=suite")

    # expect Lux Suite card text somewhere on page
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    assert "Lux Suite" in driver.page_source


def test_rooms_search_no_results(driver, base_url):
    driver.get(base_url + "/rooms?q=zzzzzzzzzz")

    empty = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-test="rooms-empty"]'))
    )
    assert "No rooms found" in empty.text


def test_rooms_filter_by_type(driver, base_url):
    """Test filtering rooms by type (Suite)."""
    driver.get(base_url + "/rooms")
    
    # Select Suite type from dropdown
    type_select = Select(driver.find_element(By.CSS_SELECTOR, '[data-test="rooms-type"]'))
    type_select.select_by_value("Suite")
    
    # Submit the filter form
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    
    # Wait for page to load
    WebDriverWait(driver, 5).until(EC.url_contains("type=Suite"))
    
    # Verify Suite rooms are shown
    assert "Lux Suite" in driver.page_source or "Pharaoh" in driver.page_source
    # Verify Single rooms are NOT shown
    assert "Cairo Comfort Single" not in driver.page_source


def test_rooms_filter_by_max_price(driver, base_url):
    """Test filtering rooms by maximum price."""
    driver.get(base_url + "/rooms")
    
    # Enter max price
    max_price_input = driver.find_element(By.CSS_SELECTOR, '[data-test="rooms-maxprice"]')
    max_price_input.clear()
    max_price_input.send_keys("70")
    
    # Submit the filter form
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    
    # Wait for page to load
    WebDriverWait(driver, 5).until(EC.url_contains("max_price=70"))
    
    # Verify cheap rooms are shown (Cairo Comfort Single $55, Aswan Desert Oasis $65)
    assert "Cairo Comfort Single" in driver.page_source or "Aswan Desert Oasis" in driver.page_source
    # Verify expensive rooms are NOT shown
    assert "Lux Suite" not in driver.page_source  # $160
    assert "Pharaoh" not in driver.page_source  # $220


def test_rooms_filter_combined(driver, base_url):
    """Test combining search query with type filter."""
    driver.get(base_url + "/rooms?q=comfort&type=Single")
    
    # Wait for page to load
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
    # Should find Cairo Comfort Single (matches both query and type)
    assert "Cairo Comfort Single" in driver.page_source
    # Should NOT show Double or Suite rooms
    assert "Nile View Double" not in driver.page_source

