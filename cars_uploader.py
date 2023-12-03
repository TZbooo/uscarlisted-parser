import os
import csv
import time

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
from pydantic import BaseModel
from pyvirtualdisplay import Display


class Car(BaseModel):
    id: int
    title: str
    price: int
    description: str
    condition: str
    body: str
    make: str
    model: str
    mileage: str
    fuel_type: str
    year: str
    transmission: str
    exterior_color: str
    history: str
    vin: str


car_list = []
with open('table.csv', 'r') as csv_file:
    table = csv.reader(csv_file)

    for row in list(table)[5188:]:
        car_list.append(Car(
            id=row[0],
            title=row[1],
            price=row[2],
            description=row[3],
            condition=row[4],
            body=row[5],
            make=row[6],
            model=row[7],
            mileage=row[8],
            fuel_type=row[9],
            year=row[10],
            transmission=row[11],
            exterior_color=row[12],
            history=row[13],
            vin=row[14]
        ))


def main() -> None:
    try:
        driver = uc.Chrome(no_sandbox=True)
        driver.implicitly_wait(10)
        driver.get('http://easy2ltq.beget.tech/wp-admin/')
        driver.find_element(
            By.ID,
            'user_login'
        ).send_keys('admin')
        driver.find_element(
            By.ID,
            'user_pass'
        ).send_keys('uscars-2023' + Keys.ENTER)
        time.sleep(1)
        driver.get(
            'http://easy2ltq.beget.tech/wp-admin/post-new.php?post_type=equipment'
        )

        for car in car_list:
            print(f'{car.id=}')
            try:
                driver.find_element(
                    By.CSS_SELECTOR,
                    'h1[aria-label="Добавить заголовок"]'
                ).send_keys(car.title)
            except NoSuchElementException:
                continue
            driver.execute_script(
                'arguments[0].click();',
                driver.find_element(
                    By.CSS_SELECTOR,
                    '.acf-gallery-toolbar a'
                )
            )

            car_images = '\n'.join([
                f'{os.getcwd()}/images/{car.id}/{i}.jpg'
                for i in range(5)
            ])
            driver.find_element(
                By.CSS_SELECTOR,
                'input[type="file"]'
            ).send_keys(car_images)
            time.sleep(40)
            driver.execute_script(
                'arguments[0].click();',
                driver.find_element(
                    By.CLASS_NAME,
                    'media-button-select'
                )
            )

            driver.execute_script(
                'arguments[0].click();',
                driver.find_element(
                    By.CSS_SELECTOR,
                    '.acf-tab-group li + li > a'
                )
            )
            driver.find_element(
                By.CSS_SELECTOR,
                '.acf-fields .acf-field:nth-child(5) input'
            ).send_keys(car.price)
            driver.find_element(
                By.CSS_SELECTOR,
                '.acf-fields .acf-field:nth-child(6) select'
            ).send_keys(car.condition)
            driver.find_element(
                By.CSS_SELECTOR,
                '.acf-fields .acf-field:nth-child(7) select'
            ).send_keys(car.body)
            driver.find_element(
                By.CSS_SELECTOR,
                '.acf-fields .acf-field:nth-child(8) select'
            ).send_keys(car.make)
            driver.find_element(
                By.CSS_SELECTOR,
                '.acf-fields .acf-field:nth-child(9) input'
            ).send_keys(car.model)
            driver.find_element(
                By.CSS_SELECTOR,
                '.acf-fields .acf-field:nth-child(10) input'
            ).send_keys(car.mileage)
            driver.find_element(
                By.CSS_SELECTOR,
                '.acf-fields .acf-field:nth-child(11) select'
            ).send_keys(car.fuel_type)
            driver.find_element(
                By.CSS_SELECTOR,
                '.acf-fields .acf-field:nth-child(12) select'
            ).send_keys(car.year)
            driver.find_element(
                By.CSS_SELECTOR,
                '.acf-fields .acf-field:nth-child(13) select'
            ).send_keys(car.transmission)
            driver.find_element(
                By.CSS_SELECTOR,
                '.acf-fields .acf-field:nth-child(14) select'
            ).send_keys(car.exterior_color)
            driver.find_element(
                By.CSS_SELECTOR,
                '.acf-fields .acf-field:nth-child(15) select'
            ).send_keys(car.history)
            driver.find_element(
                By.CSS_SELECTOR,
                '.acf-fields .acf-field:nth-child(16) input'
            ).send_keys(car.vin)

            driver.execute_script(
                'arguments[0].click();',
                driver.find_element(
                    By.CSS_SELECTOR,
                    '.acf-tab-group li + li + li > a'
                )
            )
            description_textarea = driver.find_element(
                By.CSS_SELECTOR,
                '.acf-fields .acf-field:nth-child(22) textarea'
            )
            driver.execute_script(
                'arguments[0].value = arguments[1]',
                description_textarea,
                car.description
            )

            try:
                driver.execute_script(
                    'arguments[0].click();',
                    driver.find_element(
                        By.CSS_SELECTOR,
                        'button[aria-controls="edit-post:document"][aria-label="Настройки"][aria-expanded="false"]'
                    )
                )
            except NoSuchElementException:
                pass

            driver.find_element(
                By.CLASS_NAME,
                'components-form-token-field__input'
            ).send_keys('cars' + Keys.ENTER)

            for i in range(1):
                driver.execute_script(
                    'arguments[0].click();',
                    driver.find_elements(
                        By.CSS_SELECTOR,
                        '.editor-post-publish-button__button'
                    )[i]
                )
            time.sleep(2.5)
            driver.get(
                'http://easy2ltq.beget.tech/wp-admin/post-new.php?post_type=equipment'
            )
            try:
                driver.switch_to.alert.accept()
            except NoAlertPresentException:
                pass
            time.sleep(1)
    finally:
        driver.quit()


if __name__ == '__main__':
    try:
        display = Display(size=(1920, 1080))
        display.start()
        print('DISPLAY START')
        main()
    finally:
        display.stop()
        pass
