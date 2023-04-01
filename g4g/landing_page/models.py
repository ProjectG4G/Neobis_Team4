from django.db import models

class LandingPage(models.Model):
    title1 = models.CharField(max_length=250)
    block1 = models.TextField()
    block2 = models.TextField()
    block3 = models.TextField()
    block4 = models.TextField()
    images1 = models.ImageField(upload_to='images/landing_page/', null=True)
    title2 = models.CharField(max_length=250)
    block5 = models.TextField()
    block6 = models.TextField()
    block7 = models.TextField()
    block8 = models.TextField()
    block9 = models.TextField()
    block10 = models.TextField()
    images2 = models.ImageField(upload_to='images/landing_page/', null=True)
    images3 = models.ImageField(upload_to='images/landing_page/', null=True)

    links = models.URLField()
