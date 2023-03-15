import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from geoapi.models import Region, District, Village, Country


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
    def get_district_list(region) -> dict[str:int]:
        if not region:
            district_names = District.objects.values_list('id', 'name', 'type')
        else:
            district_names = District.objects.filter(region__name=region).values_list('id', 'name', 'type')

        districts = {}

        for data in district_names:
            if data[2] == 1:
                districts[data[1] + ' району'] = data[0]
            else:
                districts[data[1] + ' шаары'] = data[0]

        return districts

    @staticmethod
    def get_villages_list(district) -> dict[str:int]:
        print(district)
        if 'шаары' in district:
            village_names = Village.objects.filter(
                district__name=extract(district),
                district__type=2
            ).values_list('id', 'name')
        else:
            village_names = Village.objects.filter(
                district__name=extract(district),
                district__type=1
            ).values_list('id', 'name')

        villages = {data[1] + " айылы": data[0] for data in village_names}
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
