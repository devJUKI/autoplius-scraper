from autoplius_scraper import AutopliusScraper
from database import Database
import time
import traceback


def setup_foreign_key(table, value):
    if value == "" or value == -1 or value == None:
        return None

    db_row = database.select_data(
        table, 'id', f'name = \'{value}\'')
    if len(db_row) == 0:
        data = {
            "name": value
        }
        id = database.insert_data(table, data)
    else:
        id = db_row[0][0]

    return id


make_id = 97  # BMW
model_id = 1313  # 5-series

autoplius_scraper = AutopliusScraper()

# Don't scrape all data with one driver?
# Do loop, that takes 1k entries with one iteration
time2 = time.time()

cars = []
try:
    cars = autoplius_scraper.scrape_ads(1)
except Exception:
    traceback.print_exc()

time1 = time.time()

autoplius_scraper.quit_driver()


database = Database('localhost', 'root', '', 'car_ads')
print(f'Cars found: {len(cars)}')
if (len(cars) > 0):
    for car in cars:
        print(car)

        fuel_type_id = setup_foreign_key('fuel_type', car.fuel_type)
        body_type_id = setup_foreign_key('body_type', car.body_type)
        door_count_id = setup_foreign_key('door_count', car.door_count)
        drivetrain_id = setup_foreign_key('drivetrain', car.drivetrain)
        transmission_id = setup_foreign_key('transmission', car.transmission)
        color_id = setup_foreign_key('color', car.color)
        steering_id = setup_foreign_key('steering', car.steering)
        make_id = setup_foreign_key('make', car.make)

        model_query_results = database.select_data(
            'model', 'id', f'name = \'{car.model}\'')
        if len(model_query_results) == 0:
            data = {
                'name': car.model,
                'fk_make': make_id
            }
            model_id = database.insert_data('model', data)
        else:
            model_id = model_query_results[0][0]

        # Need to add values as foreign keys
        data = {
            "production_date": car.production_date,
            "mileage": car.mileage,
            "engine": car.engine,
            "horse_power": car.horse_power,
            "seat_count": car.seat_count,
            "fuel_type": fuel_type_id,
            "body_type": body_type_id,
            "door_count": door_count_id,
            "drivetrain": drivetrain_id,
            "transmission": transmission_id,
            "color": color_id,
            "steering": steering_id,
            "fk_model": model_id
        }
        #database.insert_data('car', data)


print('Done')

print(time1 - time2)
