# Generated by Django 3.2.22 on 2023-11-05 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_report', '0004_alter_detailspatient_created_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailspatient',
            name='created_date',
            field=models.DateField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='detailspatient',
            name='created_time',
            field=models.TimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
    ]