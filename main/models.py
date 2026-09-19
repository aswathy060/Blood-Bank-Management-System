from django.db import models


class Donor(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    blood_group = models.CharField(max_length=5)
    units = models.IntegerField(default=1)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.name


class BloodRequest(models.Model):
    hospital = models.CharField(max_length=150)
    patient_id = models.CharField(max_length=20, null=True, blank=True)
    patient_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=5)
    units = models.IntegerField()
    request_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return self.patient_name


class BloodStock(models.Model):
    blood_group = models.CharField(max_length=5, unique=True)
    units = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.blood_group} - {self.units} units"