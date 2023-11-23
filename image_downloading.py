import os
import shutil
import csv

import requests


try:
    shutil.rmtree('images')
except FileNotFoundError:
    pass
os.mkdir('images')

with open('table.csv', 'r') as csv_file:
    table = csv.reader(csv_file)

    for row in list(table)[1:]:
        car_id = row[0]
        car_image_url_list = [url for url in row[15].split(',\n') if url]

        os.mkdir(f'images/{car_id}')
        for i, url in enumerate(car_image_url_list):
            with open(f'images/{car_id}/{i}.jpg', 'wb') as image_file:
                image_file.write(requests.get(url).content)
