# Generated by Django 4.2.2 on 2023-10-04 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaapp', '0008_assreviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='assreviews',
            name='sentiment',
            field=models.CharField(default='', max_length=15),
        ),
    ]
