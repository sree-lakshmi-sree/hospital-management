# Generated by Django 4.1.7 on 2023-03-23 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='token',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
    ]
