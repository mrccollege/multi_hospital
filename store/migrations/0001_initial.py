# Generated by Django 3.2.22 on 2023-11-09 04:32

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
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_hospital_user', to='accounts.hospitaluser')),
                ('main_store_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_store_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'main_store',
            },
        ),
        migrations.CreateModel(
            name='MiniStore',
            fields=[
                ('mini_store_id', models.AutoField(primary_key=True, serialize=False)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mini_hospital_user', to='accounts.hospitaluser')),
                ('mini_store_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mini_store_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'mini_store',
            },
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('medicine_id', models.AutoField(primary_key=True, serialize=False)),
                ('batch_no', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.IntegerField()),
                ('qty', models.IntegerField()),
                ('expiration', models.DateField()),
                ('manufacturer', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('main_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mapping_main_store_user', to='store.mainstore')),
            ],
            options={
                'db_table': 'main_store_medicine',
            },
        ),
        migrations.CreateModel(
            name='MappingMiniStorMedicine',
            fields=[
                ('mapping_id', models.AutoField(primary_key=True, serialize=False)),
                ('mini_qty', models.IntegerField()),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mapping_mini_store_medicine', to='store.medicine')),
                ('mini_store_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mapping_mini_store_user', to='store.ministore')),
            ],
            options={
                'db_table': 'mapping_mini_store_medicine',
            },
        ),
        migrations.CreateModel(
            name='MainMedicalStoreMedicineTransactionHistory',
            fields=[
                ('medicine_trans_id', models.AutoField(primary_key=True, serialize=False)),
                ('trans_qty', models.IntegerField()),
                ('trans_created', models.DateField(auto_now_add=True)),
                ('trans_update', models.DateField(null=True)),
                ('mapping_medicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.medicine')),
            ],
            options={
                'db_table': 'main_store_medicine_transaction_history',
            },
        ),
    ]
