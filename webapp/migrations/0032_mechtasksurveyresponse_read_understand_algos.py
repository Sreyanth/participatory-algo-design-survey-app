# Generated by Django 3.1.7 on 2021-10-12 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0031_auto_20210901_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='mechtasksurveyresponse',
            name='read_understand_algos',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
