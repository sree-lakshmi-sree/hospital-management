from django.db import models
# Create your models here.


class Department(models.Model):
    name = models.CharField(primary_key=True,max_length=20,unique=True)

class Doctor(models.Model):
    name = models.CharField(max_length=20)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    op_start_time = models.TimeField()
    op_end_time = models.TimeField()
    consultation_charge = models.IntegerField()


class Customer(models.Model):
    name = models.CharField(max_length=50)


class Admin(models.Model):
    user_name = models.CharField(max_length=15)
    password = models.CharField(max_length=10)
    token = models.CharField(
        max_length=20, default=None, blank=True, null=True)
