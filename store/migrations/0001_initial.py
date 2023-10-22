# Generated by Django 3.2.22 on 2023-10-22 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainMedicalStore',
            fields=[
                ('main_id', models.AutoField(primary_key=True, serialize=False)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitaluser')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'main_medical_store',
            },
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('main_medicine_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('manufacturer', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField()),
                ('expiration_date', models.DateField()),
                ('main_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.mainmedicalstore')),
            ],
            options={
                'db_table': 'medicine',
            },
        ),
        migrations.CreateModel(
            name='MiniMedicalStore',
            fields=[
                ('mini_id', models.AutoField(primary_key=True, serialize=False)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitaluser')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'mini_medical_store',
            },
        ),
        migrations.CreateModel(
            name='MiniStoreMedicine',
            fields=[
                ('mini_medicine_id', models.AutoField(primary_key=True, serialize=False)),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.medicine')),
                ('mini_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.minimedicalstore')),
            ],
            options={
                'db_table': 'mini_store_medicine',
            },
        ),
    ]
