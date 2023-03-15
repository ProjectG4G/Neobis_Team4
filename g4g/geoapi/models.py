from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"


class Region(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    city_district = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)

    DISTRICT_TYPES = (
        (1, 'District'),
        (2, 'City'),
    )

    type = models.IntegerField(choices=DISTRICT_TYPES, default=1, null=False)

    def __str__(self):
        if self.type == 1:
            return self.name + ' району'
        else:
            return self.name + ' шаары'


class Village(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
