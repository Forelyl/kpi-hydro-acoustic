import pytest
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import os
import re


def get_test_dir():
    """
    Adjust the current working directory (cwd) to the main git directory
    using a regular expression to find it in the path.
    """
    target_dir = "kpi-hydro-acoustic"
    current_path = os.getcwd()

    # Regex to match the target directory and anything following it
    match = re.search(rf"(.*?{re.escape(target_dir)})", current_path)

    if match:
        # Extract the path up to and including the target directory
        new_cwd = match.group(1)
        return new_cwd + "/Backend/test"
    else:
        pytest.fail(f"'{target_dir}' directory not found in the current working directory tree.")


@pytest.fixture()
def test_setup():
    global driver
    driver = webdriver.Chrome()
    driver.get("http://localhost:5173/")
    yield
    driver.close()
    driver.quit()


def test_separate_tracks_checkbox(test_setup):
    checkboxes: list[WebElement] = driver.find_elements(By.XPATH, "//input[@type='checkbox']")

    assert len(checkboxes) != 0, "No elements were found with input[@type='checkbox']"
    assert len(checkboxes) == 1, "More than one element was found with input[@type='checkbox']"

    checkbox = checkboxes[0]

    # -----
    # select checkbox
    # -----

    driver.execute_script("document.getElementById('separate_tracks').children[0].click()")
    assert checkbox.is_selected(), "Checkbox is not checked"


def test_button_change_states(test_setup):
    try:
        button: WebElement = driver.find_element(By.TAG_NAME, "button")
    except NoSuchElementException:
        pytest.fail("Button was no found on main page")

    assert not button.is_enabled(), "Button is enabled, yet shouldn't"

    # -----
    # upload file
    # -----
    file_input = driver.find_element(By.XPATH, "//input[@type='file']")
    file_input.send_keys(get_test_dir() + "/test-data/test_file.wav")
    try:
        WebDriverWait(driver, 2).until(lambda driver: button.is_enabled())
    except TimeoutException:
        pytest.fail("Button is not enabled in 2 seconds, yet should be")


# =============================================================================
# Pipline
# =============================================================================

@pytest.fixture()
def test_setup_pipeline(test_setup):
    # -----
    # upload file

    try:
        button: WebElement = driver.find_element(By.TAG_NAME, "button")
    except NoSuchElementException:
        pytest.fail("Button was no found on main page")

    file_input = driver.find_element(By.XPATH, "//input[@type='file']")
    file_input.send_keys(get_test_dir() + "/test-data/test_file.wav")
    try:
        WebDriverWait(driver, 2).until(lambda driver: button.is_enabled())
    except TimeoutException:
        pytest.fail("Button is not enabled in 2 seconds, yet should be")

    # -----
    # open pipeline
    button.click()
    try:
        WebDriverWait(driver, 2).until(lambda driver: driver.current_url == "http://localhost:5173/pipeline")
    except TimeoutException:
        pytest.fail("Pipeline page was not opened in 2 seconds")

    # ----

    yield


def test_change_pipline_steps(test_setup_pipeline):
    steps = driver.find_elements(By.CLASS_NAME, "pipline_step")
    assert len(steps) == 1

    try:
        button: WebElement = driver.find_element(By.CLASS_NAME, "add_step")
    except NoSuchElementException:
        pytest.fail("Add step button was no found on pipeline page")
    button.click()

    steps = driver.find_elements(By.CLASS_NAME, "pipline_step")
    assert len(steps) == 2

    buttons: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, "div.top_part > div > div:has(>svg)")
    assert len(buttons) == 2, "Remove step buttons should be present"

    button = buttons[1]
    button.click()

    steps = driver.find_elements(By.CLASS_NAME, "pipline_step")
    assert len(steps) == 1


# =============================================================================
# Download
# =============================================================================
def test_get_to_download_page(test_setup_pipeline):
    delete_button: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, ".top_part > div > div:has(>svg)")
    assert len(delete_button) == 1, "Zero or more than one button was found on first opening of pipeline page"

    delete_button[0].click()

    next_button: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, "#send_button")
    assert len(next_button) == 1, "Zero or more than one send button was found on first opening of pipeline page"

    next_button[0].click()
    try:
        WebDriverWait(driver, 10).until(lambda driver: driver.current_url == "http://localhost:5173/download")
    except TimeoutException:
        pytest.fail("Download page was not opened in 2 seconds")