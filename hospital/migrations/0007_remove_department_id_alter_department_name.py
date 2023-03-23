# Generated by Django 4.1.7 on 2023-03-23 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0006_alter_department_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='id',
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, unique=True),
        ),
    ]
