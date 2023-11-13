from django.db import models

# Create your models here.
from accounts.models import HospitalUser


class LookupField(models.Model):
    hospital = models.ForeignKey(HospitalUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=True, blank=True)
    code = models.CharField(max_length=256, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    video = models.FileField(null=True, blank=True)
    pdf = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'lookup_field'
