# Generated by Django 3.1.7 on 2021-08-26 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0028_auto_20210826_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='mechtasksurveyresponse',
            name='base_rate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]