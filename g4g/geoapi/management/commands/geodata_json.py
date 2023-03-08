import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from geoapi.models import Region, District, City, Village, Country


def extract(name):
    return name.split()[0]


class Command(BaseCommand):
    help = 'export geodata to json'

    @staticmethod
    def get_region_list() -> list[str]:
        region_names = Region.objects.values_list('name')

        regions = [name[0] for name in region_names]

        return regions

    @staticmethod
    def get_district_list(region) -> list[str]:
        if not region:
            district_names = District.objects.values_list('name')
            city_names = City.objects.values_list('name')

            districts = [name[0] + " району" for name in district_names]
            districts += [name[0] + " шаары" for name in city_names]

            return districts

        district_names = District.objects.filter(region__name=region).values_list('name')
        city_names = City.objects.filter(region__name=region).values_list('name')

        districts = [name[0] + " району" for name in district_names]
        districts += [name[0] + " шаары" for name in city_names]

        return districts

    @staticmethod
    def get_villages_list(district) -> list[str]:
        if 'шаары' in district:
            village_names = Village.objects.filter(city__name=extract(district)).values_list('name')
        else:
            village_names = Village.objects.filter(district__name=extract(district)).values_list('name')

        villages = [name[0] + " айылы" for name in village_names]

        return villages

    def handle(self, *args, **options):
        region_list = self.get_region_list()
        district_list = self.get_district_list(None)

        data = {
            'regions': region_list,
            'districts': {
                region_list[i]: self.get_district_list(region_list[i]) for i in range(7)
            },
            'villages': {
                district: self.get_villages_list(district) for district in district_list
            }
        }

        json_object = json.dumps(data, ensure_ascii=False)
        with open(os.path.join(settings.BASE_DIR, 'static/geodata/geodata.json'), 'w') as file:
            file.write(json_object)
