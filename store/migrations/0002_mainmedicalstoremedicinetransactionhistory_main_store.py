# Generated by Django 3.2.22 on 2023-11-09 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainmedicalstoremedicinetransactionhistory',
            name='main_store',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='main_trans_main_store_user', to='store.mainstore'),
            preserve_default=False,
        ),
    ]