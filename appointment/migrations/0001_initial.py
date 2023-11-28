# Generated by Django 3.2.22 on 2023-11-28 04:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientAppointment',
            fields=[
                ('patient_appoint_id', models.AutoField(primary_key=True, serialize=False)),
                ('bloodPressure', models.CharField(blank=True, max_length=10, null=True)),
                ('pulses', models.IntegerField(blank=True, default=72, null=True)),
                ('weight', models.CharField(blank=True, max_length=10, null=True)),
                ('fees', models.IntegerField(blank=True, default=0, null=True)),
                ('paid_free', models.CharField(blank=True, max_length=10, null=True)),
                ('cash', models.IntegerField(blank=True, default=0, null=True)),
                ('online', models.IntegerField(blank=True, default=0, null=True)),
                ('remaining', models.IntegerField(blank=True, default=0, null=True)),
                ('appointment_date', models.DateField(blank=True, default=None, null=True)),
                ('appointment_time', models.TimeField(blank=True, default=None, null=True)),
                ('appoint_status', models.CharField(default='unchecked', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('appoint_ward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.hospitalappointmentvisit')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.doctoruser')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitaluser')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.patientuser')),
            ],
            options={
                'db_table': 'patient_appointment',
            },
        ),
    ]
