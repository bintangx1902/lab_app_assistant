# Generated by Django 4.2.8 on 2024-03-09 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presence', '0019_auto_20220921_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='generateqrcode',
            name='assistance',
            field=models.CharField(default='', max_length=255),
        ),
    ]