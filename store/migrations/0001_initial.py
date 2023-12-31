# Generated by Django 3.2.22 on 2023-11-28 04:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('medicine_id', models.AutoField(primary_key=True, serialize=False)),
                ('batch_no', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.IntegerField(default=0)),
                ('expiration', models.DateField(null=True)),
                ('manufacturer', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(null=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Medicine_hospital', to='accounts.hospitaluser')),
                ('main_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Medicine_main_store', to='accounts.stores')),
            ],
            options={
                'db_table': 'medicine',
            },
        ),
        migrations.CreateModel(
            name='MiniStoreMedicine',
            fields=[
                ('mini_pro_id', models.AutoField(primary_key=True, serialize=False)),
                ('qty', models.IntegerField(null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(null=True)),
                ('from_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MiniStoreMedicine_from_store', to='accounts.stores')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MiniStoreMedicine_hospital', to='accounts.hospitaluser')),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MiniStoreMedicine_medicine', to='store.medicine')),
                ('to_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MiniStoreMedicine_to_store', to='accounts.stores')),
            ],
            options={
                'db_table': 'mini_store_medicine',
            },
        ),
        migrations.CreateModel(
            name='MedicineTransferHistory',
            fields=[
                ('trans_pro_id', models.AutoField(primary_key=True, serialize=False)),
                ('qty', models.IntegerField(null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(null=True)),
                ('from_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MedicineTransferHistory_from_store', to='accounts.stores')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MedicineTransferHistory_hospital', to='accounts.hospitaluser')),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MedicineTransferHistory_medicine', to='store.medicine')),
                ('to_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MedicineTransferHistory_to_store', to='accounts.stores')),
            ],
            options={
                'db_table': 'medicine_transfer_history',
            },
        ),
        migrations.CreateModel(
            name='MainStoreMedicine',
            fields=[
                ('main_pro_id', models.AutoField(primary_key=True, serialize=False)),
                ('qty', models.IntegerField(default=0, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(null=True)),
                ('from_mini_store', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='MainStoreMedicine_from_mini_store', to='accounts.stores')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MainStoreMedicine_hospital', to='accounts.hospitaluser')),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MainStoreMedicine_medicine', to='store.medicine')),
                ('to_main_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MainStoreMedicine_to_main_store', to='accounts.stores')),
            ],
            options={
                'db_table': 'main_store_medicine',
            },
        ),
    ]
