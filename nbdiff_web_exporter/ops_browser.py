from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def connect(url, download_dir: str):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": download_dir,
            "download.directory_upgrade": True,
            "download.prompt_for_download": False,
        },
    )

    driver = Chrome(options=options)
    driver.set_window_size("1200", "10000")
    driver.get(url)
    return driver


def close(driver: Chrome, timeout: int = 10):
    _ = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, "nbdime-close"))
    )
    download_button = driver.find_element(By.ID, "nbdime-close")
    download_button.click()
    return


def export(driver: Chrome, timeout: int = 10):
    _ = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, "nbdime-export"))
    )
    download_button = driver.find_element(By.ID, "nbdime-export")
    download_button.click()
    return
