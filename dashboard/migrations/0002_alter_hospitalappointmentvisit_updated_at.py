# Generated by Django 3.2.22 on 2023-11-13 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospitalappointmentvisit',
            name='updated_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]