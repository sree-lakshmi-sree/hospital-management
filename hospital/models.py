from django.db import models
# Create your models here.


class Doctor(models.Model):
    name = models.CharField(max_length=20)
    department = models.CharField(max_length=20)
    op_start_time = models.TimeField()
    op_end_time = models.TimeField()
    consultation_charge = models.IntegerField()


class Customer(models.Model):
    name = models.CharField(max_length=50)


class Admin(models.Model):
    user_name = models.CharField(max_length=15)
    password = models.CharField(max_length=10)
