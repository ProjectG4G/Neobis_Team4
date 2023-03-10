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
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class Village(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
