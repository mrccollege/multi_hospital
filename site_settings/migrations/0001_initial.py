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
            name='LookupField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=256, null=True)),
                ('code', models.CharField(blank=True, max_length=256, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='lookup_images')),
                ('video', models.FileField(blank=True, null=True, upload_to='lookup_videos')),
                ('pdf', models.FileField(blank=True, null=True, upload_to='lookup_pdfs')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitaluser')),
            ],
            options={
                'db_table': 'lookup_field',
            },
        ),
    ]
