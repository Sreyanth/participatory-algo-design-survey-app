# Generated by Django 3.1.7 on 2021-03-05 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mechtaskusergroup',
            name='slug',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
