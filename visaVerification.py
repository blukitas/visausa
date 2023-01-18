# Generated by Selenium IDE
import configparser
import pytest
import time
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class TestVisaVerification:
    """Using selenium to explore the appoitments"""

    user = None
    password = None
    base_date = '2023-07-30'

    def __init__(self):
        self.config_user()

    def config_user(
        self,
    ):
        """Get user credentials from config.ini file."""
        another_config = configparser.RawConfigParser()
        another_config.read("config.ini")
        self.user = another_config["usa_credentials"]["user"]
        self.password = another_config["usa_credentials"]["pass"]

    def __enter__(self):
        self.setup_method("get")
        return self

    def setup_method(self, method):
        """Setup webdriver for Selenium

        Args:
            method (_type_): _description_
        """
        options = Options()
        #     options.add_argument('--headless')
        #     options.add_argument('--disable-gpu')
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            + "AppleWebKit/537.36 (KHTML, like Gecko)"
            + "Chrome/87.0.4280.141 Safari/537.36"
        )

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), chrome_options=options
        )
        self.vars = {}

    def test_visaVerification(self):
        """Run the main code to get the appointment"""

        #     try:
        # Test name: Visa Verification
        # Step # | name | target | value
        # 1 | open | /es-ar/niv/users/sign_in |
        print("open site")
        self.driver.get("https://ais.usvisa-info.com/es-ar/niv/users/sign_in")
        # 2 | setWindowSize | 1512x871 |
        #         self.driver.set_window_size(1512, 871)
        # 3 | type | id=user_email | reemplazar 'email' con el email real
        # self.driver.find_element(By.ID, "user_email").send_keys("email")
        self.driver.find_element(By.ID, "user_email").send_keys(self.user)
        # 4 | type | id=user_password | reemplazar 'password' con el password real
        self.driver.find_element(By.ID, "user_password").send_keys(self.password)
        # self.driver.find_element(By.ID, "user_password").send_keys("a3^BS%Xe2X")
        # 5 | click | css=.icheckbox |
        print("login")
        self.driver.find_element(By.CSS_SELECTOR, ".icheckbox").click()
        # 6 | click | name=commit |
        self.driver.find_element(By.NAME, "commit").click()
        # 7 | click | linkText=Continuar |
        self.driver.implicitly_wait(10)
        self.driver.find_element(By.LINK_TEXT, "Continuar").click()
        # 8 | open | https://ais.usvisa-info.com/es-ar/niv/schedule/36229112/appointment |
        self.driver.get(
            "https://ais.usvisa-info.com/es-ar/niv/schedule/39718217/appointment"
        )
        # time.sleep(2)
        # 9 | click | id=appointments_asc_appointment_facility_id |
        # This is already selected
        # self.driver.find_element(By.ID, "appointments_asc_appointment_facility_id").click()
        # self.driver.find_element(By.ID, "appointments_consulate_appointment_facility_id").click()
        time.sleep(5)
        # 9.b | click | id=consulate_date_time_not_available | It seems to be a problem with the page
        elements = self.driver.find_elements(
            by=By.ID, value="consulate_date_time_not_available"
        )

        if len(elements) < 1:
            print("No appointments in starting date. Issue with the page")

            raise Exception("No appointments in starting date. Issue with the page")

        # 10 | click | id=appointments_asc_appointment_date |
        # self.driver.find_element(By.ID, "appointments_asc_appointment_date").click()

        self.driver.find_element(
            By.ID,
            "appointments_consulate_appointment_date",
        ).click()

        element = None
        while element == None:
            element = "found"
            try:
                # 11 | click | css=.ui-icon-circle-triangle-e |
                self.driver.find_element(
                    By.CSS_SELECTOR, ".ui-icon-circle-triangle-e"
                ).click()
                # 12 | click | xpath=//td[@data-handler='selectDay']/a |
                self.driver.find_element(
                    By.XPATH, "//td[@data-handler='selectDay']/a"
                ).click()
            except Exception:
                # TODO: Check exception
                element = None
        # 13 | click | id=appointments_asc_appointment_time |
        self.driver.find_element(
            By.ID, "appointments_consulate_appointment_time"
        ).click()
        # 14 | select | id=appointments_asc_appointment_time | label=09:45
        dropdown = Select(
            self.driver.find_element(By.ID, "appointments_consulate_appointment_time")
        )
        #         dropdown.find_element(By.XPATH, "//option[. = '09:45']").click()
        # Don't find the index
        # dropdown.select_by_index(0).click()
        print("appointments_consulate_appointment_time")
        selected_time = None
        times = [
            "08:00",
            "08:30",
            "09:00",
            "09:30",
            "10:00",
            "10:30",
            "11:00",
        ]
        i = 0
        while selected_time is None:
            selected_time = "true"
            try:
                print(f"times['i'] > {times[i]}")
                dropdown.select_by_value(times[i])
                # dropdown.select_by_value(times[i]).click()
            except AttributeError as error:
                print("handling specific exception - attribute error")
                print(error)
            # except NoSuchElementException as error:
            except IndexError as error:
                print(error)
                print(f"exeption class: {type(error)}")
                break
            except Exception as error:
                print(error)
                print(f"exeption class: {type(error)}")
                selected_time = None
                i += 1

        # If there is no second appointment available (id = "asc_date_time_not_available")
        #   Return, and find next (put min_date, max_date)
        
        #  Check date -> appointments_consulate_appointment_date
        print("appointments_consulate_appointment_date")
        print(self.driver.find_element(By.ID, "appointments_consulate_appointment_date").get_attribute("value"))
        if (self.driver.find_element(By.ID, "appointments_consulate_appointment_date").get_attribute("value")) < self.base_date:
            print("NEWER DATE")
        else:
            print("OLDER DATE")
        # Check if message is there
        # print("len(self.driver.find_elements(By.ID, 'asc_date_time_not_available'))")
        # print(len(self.driver.find_elements(By.ID, "asc_date_time_not_available")))
        error_messages =self.driver.find_elements(By.ID, "asc_date_time_not_available")
        if len(error_messages) > 0:
            print(f'error_messages[0].value_of_css_property("display") {error_messages[0].value_of_css_property("display")}')
            if error_messages[0].value_of_css_property("display") != "None":
                # FIX: Is not working proper
                print("No appointments with this date")
            # Raise exception? Or try again?
            # Finish?

    
        # 1x | click | id=appointments_asc_appointment_date |
        # self.driver.find_element(By.ID, "appointments_asc_appointment_date").click()
        time.sleep(5)
        self.driver.find_element(By.ID, "appointments_asc_appointment_date").click()

        element = None
        while element == None:
            element = "found"
            try:
                # 11 | click | css=.ui-icon-circle-triangle-e |
                self.driver.find_element(
                    By.CSS_SELECTOR, ".ui-icon-circle-triangle-e"
                ).click()
                # 12 | click | xpath=//td[@data-handler='selectDay']/a |
                self.driver.find_element(
                    By.XPATH, "//td[@data-handler='selectDay']/a"
                ).click()
            except Exception:
                # TODO: Check exception
                element = None

        # 13 | click | id=appointments_asc_appointment_time |
        # self.driver.find_element(By.ID, "asc-appointment-fields").click()

        # 14 | select | id=appointments_asc_appointment_time | label=09:45
        dropdown = Select(
            self.driver.find_element(By.ID, "appointments_asc_appointment_time")
        )
        #         dropdown.find_element(By.XPATH, "//option[. = '09:45']").click()
        # Don't find the index
        # dropdown.select_by_index(0).click()

        # print("appointments_asc_appointment_time")
        selected_time = None
        times = []
        for hora in range(7, 15):
            for minutos in ["00", "15", "30", "45"]:
                times.append(f"{str(hora)}:{minutos}")
                # print(times[-1])

        i = 0
        while selected_time is None:
            selected_time = "true"
            try:
                print(f"times['i'] > {times[i]}")
                dropdown.select_by_value(times[i])
                # dropdown.select_by_value(times[i]).click()
            except AttributeError as error:
                print("handling specific exception - attribute error")
                print(error)
            # except NoSuchElementException as error:

            except Exception as error:
                print(error)
                print(f"exeption class: {type(error)}")
                selected_time = None
                i += 1

        # If there is appointment
        # Second dropdown: appointments_asc_appointment_date (2do combo)
        #                  appointments_consulate_appointment_date (1er combo)
        # Same code, check date, check hour

        # If all good, click: 'appointments_submit'
        print("fin")


    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Quit driver"""
        # self.driver.quit()


if __name__ == "__main__":
    print("Execution as script")
    with TestVisaVerification() as obj:
        print("Starting context manager")
        obj.test_visaVerification()
