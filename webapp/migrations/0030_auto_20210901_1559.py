# Generated by Django 3.1.7 on 2021-09-01 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0029_mechtasksurveyresponse_base_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='mechtasksurveyresponse',
            name='model_estimate_average_error_when_user_did_not_select_model',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='mechtasksurveyresponse',
            name='model_estimate_confidence_when_user_did_not_select_model',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]