from faker import Faker
import random

fake = Faker()

names = ["John Doe", "Jane Smith", "Mike Johnson", "Emily Davis", "Chris Brown", "John Smith", "Linda Martinez", "David Lee", "Susan Wilson", "Robert Johnson", "John Carter", "Jane Davis", "Mike Brown", "Emily Johnson", "Chris Taylor"]
streets = ["Oak Avenue", "Elm Street", "Maple Lane", "Cedar Drive", "Willow Way", "Spruce Court", "Aspen Road"]
cities = ["Springfield", "Shelbyville", "Ogdenville", "North Haverbrook", "Brockway", "Capital City"]

with open('fake_data.txt', 'w') as f:
    for i in range(1, 101):
        name = random.choice(names)
        street = random.choice(streets)
        city = random.choice(cities)
        address = f"{fake.building_number()} {street}, {city}"
        created_at = fake.date_time_this_year().strftime('%Y-%m-%dT%H:%M:%S')
        latitude = round(random.uniform(25.0, 50.0), 4)
        longitude = round(random.uniform(-125.0, -70.0), 4)
        f.write(f"{i}|{name}|{address}|{created_at}|{latitude}|{longitude}\n")
