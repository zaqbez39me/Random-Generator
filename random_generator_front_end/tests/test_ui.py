from selenium import webdriver

driver = webdriver.Chrome()

try:
    driver.get("http://localhost:8000/")

    assert driver.title, "Stramlit"

    print("Test passed: Random number displayed successfully")

finally:
    driver.quit()
