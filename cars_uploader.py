import csv
import time

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from pydantic import BaseModel


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
    year: int
    transmission: str
    exterior_color: str
    history: str
    vin: str


car_list = []
with open('table.csv', 'r') as csv_file:
    table = csv.reader(csv_file)

    for row in list(table)[1:501]:
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
        driver = uc.Chrome(
            user_data_dir='selenium',
            driver_executable_path='./chromedriver',
            version_main=117,
            no_sandbox=True
        )
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

        for car in car_list:
            print(f'{car.id=}')
            driver.get('http://easy2ltq.beget.tech/wp-admin/post-new.php?post_type=equipment')
            driver.find_element(
                By.CSS_SELECTOR,
                'h1[aria-label="Добавить заголовок"]'
            ).send_keys(car.title)
            driver.execute_script(
                'arguments[0].click();',
                driver.find_element(
                    By.CSS_SELECTOR,
                    '.acf-gallery-toolbar a'
                )
            )

            car_images = '\n'.join([
                f'/home/helloworldbooo/Documents/Projects/uscarlisted-parser/images/{car.id}/{i}.jpg'
                for i in range(5)
            ])
            driver.find_element(
                By.CSS_SELECTOR,
                'input[type="file"]'
            ).send_keys(car_images)
            time.sleep(10)
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
            driver.find_element(
                By.CSS_SELECTOR,
                '.acf-fields .acf-field:nth-child(22) textarea'
            ).send_keys(car.description)

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
            time.sleep(0.2)
    finally:
        driver.quit()


if __name__ == '__main__':
    main()