# Generated by Django 3.2.22 on 2023-10-28 04:29

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
            name='MainStore',
            fields=[
                ('main_store_id', models.AutoField(primary_key=True, serialize=False)),
                ('hospital_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_hospital_user', to='accounts.hospitaluser')),
                ('main_store_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_store_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'main_store',
            },
        ),
        migrations.CreateModel(
            name='MappingMedicine',
            fields=[
                ('mapping_id', models.AutoField(primary_key=True, serialize=False)),
                ('main_qty', models.IntegerField()),
                ('price', models.IntegerField()),
                ('expiration', models.DateField()),
                ('manufacturer', models.CharField(blank=True, max_length=100, null=True)),
                ('main_store_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mapping_main_store_user', to='store.mainstore')),
            ],
            options={
                'db_table': 'mapping_medicine',
            },
        ),
        migrations.CreateModel(
            name='MappingMiniStorMedicine',
            fields=[
                ('mapping_id', models.AutoField(primary_key=True, serialize=False)),
                ('mini_qty', models.IntegerField()),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mapping_mini_store_medicine', to='store.mappingmedicine')),
                ('mini_store_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mapping_mini_store_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'mapping_mini_store_medicine',
            },
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('medicine_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'medicine',
            },
        ),
        migrations.CreateModel(
            name='MiniStore',
            fields=[
                ('main_store_id', models.AutoField(primary_key=True, serialize=False)),
                ('hospital_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mini_hospital_user', to='accounts.hospitaluser')),
                ('mini_store_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mini_store_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'mini_store',
            },
        ),
        migrations.CreateModel(
            name='MedicineTransactionHistory',
            fields=[
                ('medicine_trans_id', models.AutoField(primary_key=True, serialize=False)),
                ('trans_main_qty', models.IntegerField(default=0)),
                ('trans_mini_qty', models.IntegerField(default=0)),
                ('trans_date', models.DateTimeField(auto_now_add=True)),
                ('main_store_medicine_trans', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_store_medicine_trans', to='store.mappingmedicine')),
                ('mini_store_medicine_trans', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mini_store_medicine_trans', to='store.mappingministormedicine')),
            ],
        ),
        migrations.AddField(
            model_name='mappingmedicine',
            name='medicine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mapping_medicine', to='store.medicine'),
        ),
    ]
