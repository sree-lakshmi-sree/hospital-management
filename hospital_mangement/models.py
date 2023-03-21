from django.db import models

class Doctor():
    name = models.CharField(max_length=20)
    department = models.CharField()
    op_start_time = models.TimeField()
    op_end_time = models.TimeField()
    consultation_charge = models.IntegerField()