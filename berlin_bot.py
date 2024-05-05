import logging
import time
from pathlib import Path
from platform import system

from playsound import playsound
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

system = system()

logging.basicConfig(
    format="%(asctime)s\t%(levelname)s\t%(message)s",
    level=logging.INFO,
)


ERROR_MESSAGE = "Für die gewählte Dienstleistung sind aktuell keine Termine frei! Bitte"


class WebDriver:
    def __init__(self):
        self.driver: webdriver.Chrome

    def __enter__(self) -> webdriver.Chrome:
        logging.info("Open browser")
        # some stuff that prevents us from being locked out
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(20)  # seconds
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"  # noqa: E501
        )
        self.driver.execute_cdp_cmd(
            "Network.setUserAgentOverride",
            {
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36"  # noqa: E501
            },
        )
        return self.driver

    def __exit__(self, exc_type, exc_value, exc_tb):
        logging.info("Close browser")
        self.driver.quit()


def enter_start_page(driver: webdriver.Chrome):
    logging.info("Visit start page")
    driver.get("https://otv.verwalt-berlin.de/ams/TerminBuchen")
    driver.find_element(
        By.XPATH,
        '//*[@id="mainForm"]/div/div/div/div/div/div/div/div/div/div[1]/div[1]/div[2]/a',  # noqa: 501
    ).click()
    time.sleep(1)


def tick_off_terms(driver: webdriver.Chrome):
    logging.info("Ticking off agreement")
    driver.find_element(By.XPATH, '//*[@id="xi-div-1"]/div[4]/label[2]/p').click()
    time.sleep(1)
    driver.find_element(By.ID, "applicationForm:managedForm:proceed").click()
    time.sleep(1)


def fill_out_form(driver: webdriver.Chrome):
    logging.info("Fill out form")
    # select Colombia
    s = Select(driver.find_element(By.ID, "xi-sel-400"))
    s.select_by_visible_text("Kolumbien")
    # one person
    s = Select(driver.find_element(By.ID, "xi-sel-422"))
    s.select_by_visible_text("eine Person")
    # married
    s = Select(driver.find_element(By.ID, "xi-sel-427"))
    s.select_by_visible_text("ja")
    # nationality of partner
    s = Select(driver.find_element(By.ID, "xi-sel-428"))
    s.select_by_visible_text("Deutschland")
    time.sleep(3)

    # click on the 3rd blue card
    logging.info("Selecting card")
    n_card = 3
    driver.find_element(By.XPATH, f'//*[@id="xi-div-30"]/div[{n_card}]/label/p').click()

    # select transfer visa to new passport
    logging.info("Select radio buton")
    driver.find_element(
        By.XPATH, ".//input[@type='radio' and @value='349-0-3-99-121874']"
    ).click()


def submit_form(driver: webdriver.Chrome):
    logging.info("Submit form")
    driver.find_element(By.ID, "applicationForm:managedForm:proceed").click()


class BerlinBot:
    def on_success(self):
        logging.info("Sucess: do not close the window.")
        while True:
            playsound(str(Path.cwd() / "alarm.wav"))
            time.sleep(15)

    def run(self, n_attempts=10, time_between_attempts=20):
        with WebDriver() as driver:
            enter_start_page(driver)
            tick_off_terms(driver)
            fill_out_form(driver)
            time.sleep(2)

            # (re)try submitting the form
            for _ in range(n_attempts):
                submit_form(driver)
                if ERROR_MESSAGE not in driver.page_source:
                    self.on_success()
                time.sleep(time_between_attempts)

    def run_continously(self, attempts_per_session=10, time_between_attempts=20):
        playsound(str(Path.cwd() / "alarm.wav"))  # play sound to check if it works
        while True:
            logging.info("One more round")
            self.run(
                n_attempts=attempts_per_session,
                time_between_attempts=time_between_attempts,
            )
            time.sleep(time_between_attempts)


def main():
    BerlinBot().run_continously(attempts_per_session=10, time_between_attempts=20)


if __name__ == "__main__":
    main()
