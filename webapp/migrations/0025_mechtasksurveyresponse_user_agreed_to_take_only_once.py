# Generated by Django 3.1.7 on 2021-04-28 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0024_auto_20210426_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='mechtasksurveyresponse',
            name='user_agreed_to_take_only_once',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
