# Generated by Django 3.2.15 on 2022-10-07 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0004_studentscore'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentscore',
            name='classification',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]