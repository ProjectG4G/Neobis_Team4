import csv
import os

from django.core.management.base import BaseCommand

from geoapi.models import Region, District, City, Village, Country


def extract(name):
    return name.split()[0]


def does_exist(model, name):
    return model.objects.filter(name=name).exists()


class Command(BaseCommand):
    help = 'add geodata to databases'

    def add_regions(self):
        csv_path = os.path.join(os.path.dirname(__file__), 'region_district.csv')
        file = open(csv_path)
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            region = row['region']
            district = row['district']

            district_name = extract(district)

            if not does_exist(Region, region):
                region = Region.objects.create(country_id=1, name=region)
            else:
                region = Region.objects.get(name=region)

            if 'шаары' in district:
                if not does_exist(City, district_name):
                    City.objects.create(name=district_name, region=region)
            else:
                if not does_exist(District, district_name):
                    District.objects.create(name=district_name, region=region)

    def add_districts(self):
        csv_path = os.path.join(os.path.dirname(__file__), 'district_village.csv')
        file = open(csv_path)
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            district = row['district']
            village = row['village']

            district_name = extract(district)

            if 'шаары' in district:
                if does_exist(City, district_name):
                    city = City.objects.get(name=district_name)
                    Village.objects.create(name=village, city=city)
            else:

                if 'шаары' in village:
                    if not does_exist(City, extract(village)):
                        district = District.objects.get(name=district_name)
                        City.objects.create(name=extract(village), district=district, region=district.region)
                else:
                    district = District.objects.get(name=district_name)
                    if not does_exist(Village, village):
                        Village.objects.create(name=village, district=district)

    def handle(self, *args, **options):
        if not does_exist(Country, name='Кыргызстан'):
            Country.objects.create(name='Кыргызстан')

        self.add_regions()

        if not does_exist(City, name='Ош'):
            region = Region.objects.get(name='Ош')
            City.objects.create(name='Ош', region=region)

        if not does_exist(City, name='Бишкек'):
            region = Region.objects.get(name='Чүй')
            City.objects.create(name='Бишкек', region=region)

        self.add_districts()

        print('geodata have been added to database!')
