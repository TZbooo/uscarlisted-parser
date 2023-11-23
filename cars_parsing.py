import csv

import requests
import pyexcel

from bs4 import BeautifulSoup


def parse_car_page(car_link: str, car_count: int) -> list[str]:
    html = requests.get(car_link).text
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.select_one('h1').get_text(strip=True)
    price = soup.select_one('.price').text.replace('$', '').replace(',', '')
    description = soup.select_one('.stm-car-seller-note').get_text(
        strip=True
    ).replace('\xa0', '')

    inner_tables = soup.select('.inner-table tr')
    condition_is_used = inner_tables[0].select_one('td + td').text.strip()
    body = inner_tables[1].select_one('td + td').text.strip()
    make = inner_tables[2].select_one('td + td').text.strip()
    model = inner_tables[3].select_one('td + td').text.strip()
    mileage = inner_tables[4].select_one('td + td').text.strip()
    fuel_type = inner_tables[5].select_one('td + td').text.strip()
    year = inner_tables[6].select_one('td + td').text.strip()
    transmission = inner_tables[7].select_one('td + td').text.strip()
    exterior_color = inner_tables[8].select_one('td + td').text.strip()
    history = inner_tables[9].select_one('td + td').text.strip()
    vin = inner_tables[10].select_one('td').text.strip().replace('VIN: ', '')

    image_url_list = ',\n'.join([
        img['src'].replace('-350x205', '')
        for img in soup.select('.stm-single-image img')[5:]
    ])

    return (
        car_count,
        title,
        price,
        description,
        condition_is_used,
        body,
        make,
        model,
        mileage,
        fuel_type,
        year,
        transmission,
        exterior_color,
        history,
        vin,
        image_url_list
    )


def main() -> None:
    car_count = 0
    with open('table.csv', 'w', newline='') as csv_file:
        csv.writer(csv_file).writerow([
            'id',
            'title',
            'price',
            'description',
            'condition',
            'body',
            'make',
            'model',
            'mileage',
            'fuel_type',
            'year',
            'transmission',
            'exterior_color',
            'history',
            'vin',
            'image_url_list'
        ])
    
    for page in range(1, 1556):
        print(f'{page=}')
        html = requests.get(f'https://uscarslisted.com/listings/page/{page}/').text
        soup = BeautifulSoup(html, 'lxml')

        car_link_list = [a['href'] for a in soup.select('.title.heading-font a')]
        print(car_link_list)
        for car_link in car_link_list:
            table_row = parse_car_page(car_link, car_count)
            print(table_row)
            car_count += 1

            with open('table.csv', 'a', newline='') as csv_file:
                csv.writer(csv_file).writerow(table_row)

    sheet = pyexcel.get_sheet(file_name='table.csv', delimiter=',')
    sheet.save_as('table.xlsx')

if __name__ == '__main__':
    main()