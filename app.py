from flask import Flask, render_template, request, redirect, url_for, flash
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from fake_useragent import UserAgent
from urllib.parse import quote_plus
import logging
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


import json
import os

app = Flask(__name__)
app.secret_key = 'Your secret key here'

logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def format_facebook_url(original_url):
    encoded_url = quote_plus(original_url)
    login_url = f"https://www.facebook.com/login.php?next={encoded_url}"
    return login_url


def get_random_user_agent():
    try:
        ua = UserAgent(platforms="pc", browsers="chrome")
        return ua.random
    except Exception as e:
        logging.warning(f"Could not load user agent: {e}")
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"


def create_driver():
    logging.info('Creating WebDriver instance.')

    # Automatically install the compatible webdriver
    service = Service(ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"user-agent={get_random_user_agent()}")

    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })

    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    params = {"timezoneId": "America/Chicago"}
    driver.execute_cdp_cmd("Emulation.setTimezoneOverride", params)

    logging.info('WebDriver instance created successfully.')
    return driver


def read_credentials():
    try:
        with open('credentials.json', 'r') as file:
            credentials = json.load(file)

        return credentials
    except Exception as e:
        logging.error(f"Error reading credentials: {e}")
        return None


def login(driver, url, username, password, comment):
    try:
        driver.get(url)
        logging.info(f"Navigated to login page for URL: {url}")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        ).send_keys(username)

        driver.find_element(By.ID, "pass").send_keys(password)
        driver.find_element(By.ID, "loginbutton").click()

        logging.info("Login successful. Redirecting to original post...")
        WebDriverWait(driver, 20).until(EC.url_changes(url))

        try:
            like_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@aria-label='Like']"))
            )
            like_button.click()
            logging.info("Clicked on Like button")

            time.sleep(3)

            comment_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@aria-label='Leave a comment']"))
            )
            comment_button.click()
            logging.info("Clicked on Comment button")

            time.sleep(10)

            comment_box = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@aria-label='Write a comment…']"))
            )
            logging.info("Comment Box found")

            comment_box.send_keys(comment)
            logging.info("Comment entered")

            time.sleep(2)

            comment_box.send_keys(Keys.ENTER)
            logging.info("Comment submitted")

            return True

        except TimeoutException:
            logging.error("Timed out waiting for comment box or button")
            return False
        except NoSuchElementException:
            logging.error("Could not find comment box or button")
            return False
        except Exception as e:
            logging.error(f"Error interacting with comment box: {e}")
            return False

    except Exception as e:
        logging.error(f"Login or redirect failed: {e}")
        return False


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        comment = request.form['comment']
        credentials = read_credentials()
        if credentials:
            username = credentials['username']
            password = credentials['password']
            driver = create_driver()
            success = login(driver, format_facebook_url(url),
                            username, password, comment)
            driver.quit()
            if success:
                flash('Comment posted successfully!', 'success')
            else:
                flash('Failed to post comment.', 'danger')
        else:
            flash('Failed to read credentials.', 'danger')
        return redirect(url_for('index'))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
