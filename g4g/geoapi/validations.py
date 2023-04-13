from .models import District, Region, Village
from rest_framework import serializers


def validate_region_district(region, district):
    if not Region.objects.filter(id=region.id).exists():
        raise serializers.ValidationError(
            {"detail": "Given region {} does not exist!".format(region)}
        )

    if not District.objects.filter(id=district.id).exists():
        raise serializers.ValidationError(
            {"detail": "Given district {} does not exist!".format(district)}
        )

    if district.region != region:
        raise serializers.ValidationError(
            {
                "detail": "Given district/city {} doesn't belong to region {}".format(
                    district, region
                )
            }
        )


def validate_district_village(district, village):
    if not District.objects.filter(id=district.id).exists():
        raise serializers.ValidationError(
            {"detail": "Given district {} does not exist!".format(district)}
        )

    if village and not Village.objects.filter(id=village.id).exists():
        raise serializers.ValidationError(
            {"detail": "Given region {} does not exist!".format(village)}
        )

    if village and village.district != district:
        raise serializers.ValidationError(
            {
                "detail": "Given village {} doesn't belong to district {}".format(
                    village, district
                )
            }
        )
