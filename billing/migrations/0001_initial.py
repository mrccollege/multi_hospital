# Generated by Django 3.2.22 on 2023-11-08 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PatientBillHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine', models.CharField(max_length=1000)),
                ('qty', models.CharField(max_length=1000)),
                ('price', models.CharField(max_length=1000)),
                ('patient', models.IntegerField()),
                ('hospital', models.IntegerField()),
                ('doctor', models.IntegerField()),
                ('grand_total', models.IntegerField()),
                ('cash', models.IntegerField(default=0)),
                ('online', models.IntegerField(default=0)),
                ('remaining', models.IntegerField(default=0)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Patient_bill_history',
            },
        ),
    ]
