import csv
import os

from django.core.management.base import BaseCommand

from geoapi.models import Region, District, Village, Country


def extract(name):
    return name.split()[0]


def does_exist(model, name, district_type=None):
    if not district_type:
        return model.objects.filter(name=name).exists()
    return model.objects.filter(name=name, type=district_type).exists()


class Command(BaseCommand):
    help = 'add geodata to databases'

    @staticmethod
    def add_regions():
        csv_path = os.path.join(os.path.dirname(__file__), 'region_district.csv')
        with open(csv_path, encoding='utf-8') as file:
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
                    if not does_exist(District, district_name, district_type=2):
                        District.objects.create(name=district_name, region=region, type=2)
                else:
                    if not does_exist(District, district_name, district_type=1):
                        District.objects.create(name=district_name, region=region, type=1)

    @staticmethod
    def add_districts():
        csv_path = os.path.join(os.path.dirname(__file__), 'district_village.csv')
        with open(csv_path, encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                district = row['district']
                village = row['village']

                district_name = extract(district)

                if 'шаары' in district:
                    if does_exist(District, district_name, district_type=2):
                        city = District.objects.get(name=district_name, type=2)
                        if not Village.objects.filter(name=village, district=city).exists():
                            Village.objects.create(name=village, district=city)
                else:
                    if 'шаары' in village:
                        if not does_exist(District, extract(village), district_type=2):
                            district = District.objects.get(name=district_name, type=1)
                            District.objects.create(name=extract(village), city_district=district,
                                                    region=district.region,
                                                    type=2)
                    else:
                        district = District.objects.get(name=district_name, type=1)
                        if not Village.objects.filter(name=village, district=district).exists():
                            Village.objects.create(name=village, district=district)

    def handle(self, *args, **options):
        if not does_exist(Country, name='Кыргызстан'):
            Country.objects.create(name='Кыргызстан')

        self.add_regions()

        if not does_exist(District, name='Ош', district_type=2):
            region = Region.objects.get(name='Ош')
            District.objects.create(name='Ош', region=region, type=2)

        if not does_exist(District, name='Бишкек', district_type=2):
            region = Region.objects.get(name='Чүй')
            District.objects.create(name='Бишкек', region=region, type=2)

        self.add_districts()

        print('geodata have been added to database!')
