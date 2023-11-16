# Generated by Django 3.2.22 on 2023-11-15 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20231109_1557'),
        ('patient_report', '0001_initial'),
        ('accounts', '0006_auto_20231114_1250'),
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientBillHistoryHead',
            fields=[
                ('head_id', models.AutoField(primary_key=True, serialize=False)),
                ('cash', models.IntegerField(default=0)),
                ('online', models.IntegerField(default=0)),
                ('remaining', models.IntegerField(default=0)),
                ('grand_total', models.IntegerField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(null=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.doctoruser')),
                ('header_patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_report.headerpatient')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitaluser')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.patientuser')),
            ],
            options={
                'db_table': 'patient_bill_history_head',
            },
        ),
        migrations.CreateModel(
            name='PatientBillHistoryDetails',
            fields=[
                ('detail_id', models.AutoField(primary_key=True, serialize=False)),
                ('qty', models.CharField(max_length=1000)),
                ('price', models.CharField(max_length=1000)),
                ('total', models.IntegerField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(null=True)),
                ('head', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.patientbillhistoryhead')),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.medicine')),
            ],
            options={
                'db_table': 'patient_bill_history_details',
            },
        ),
    ]