# Generated by Django 3.2.22 on 2023-11-13 02:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('billing', '0001_initial'),
        ('patient_report', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientbillhistory',
            name='header_patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_report.headerpatient'),
        ),
    ]
