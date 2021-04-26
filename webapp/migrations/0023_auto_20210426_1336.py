# Generated by Django 3.1.7 on 2021-04-26 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0022_mechtaskusergroup_use_freely'),
    ]

    operations = [
        migrations.AddField(
            model_name='mechtasksurveyresponse',
            name='passed_algo_attr_attention_check',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mechtaskusergroup',
            name='algo_attr_attention_check_statement',
            field=models.CharField(default='', max_length=500),
        ),
    ]
