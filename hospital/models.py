from django.db import models
# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=40,unique=True)
    description = models.CharField(null=True, blank=True, max_length=500)

class Doctor(models.Model):
    name = models.CharField(max_length=20)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    op_start_time = models.TimeField()
    op_end_time = models.TimeField()
    active_days = models.JSONField(null=True)
    consultation_charge = models.IntegerField()


class Customer(models.Model):
    name = models.CharField(max_length=50)


class Admin(models.Model):
    user_name = models.CharField(max_length=15)
    password = models.CharField(max_length=10)
    token = models.CharField(
        max_length=20, default=None, blank=True, null=True)
