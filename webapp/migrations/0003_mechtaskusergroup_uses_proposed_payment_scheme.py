# Generated by Django 3.1.7 on 2021-03-05 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_mechtaskusergroup_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='mechtaskusergroup',
            name='uses_proposed_payment_scheme',
            field=models.BooleanField(default=False),
        ),
    ]
