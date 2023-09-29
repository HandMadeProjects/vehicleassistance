# Generated by Django 4.2.2 on 2023-09-29 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='allLocations',
            fields=[
                ('U_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(default='', max_length=100)),
                ('locationlat', models.CharField(default='', max_length=100)),
                ('locationlong', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('U_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(default='', max_length=100)),
                ('fullname', models.CharField(default='', max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('age', models.IntegerField()),
                ('date_of_birth', models.DateField()),
                ('locationlat', models.CharField(default='', max_length=100)),
                ('locationlong', models.CharField(default='', max_length=100)),
                ('contact_number', models.CharField(default='', max_length=15)),
                ('registerdOn', models.CharField(default='', max_length=100)),
            ],
        ),
    ]
