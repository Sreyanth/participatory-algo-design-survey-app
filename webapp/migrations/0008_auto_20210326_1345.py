# Generated by Django 3.1.7 on 2021-03-26 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_auto_20210322_1406'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mechtaskstudentsample',
            old_name='computer_for_schoolwork',
            new_name='computerForSchoolwork',
        ),
        migrations.RenameField(
            model_name='mechtaskstudentsample',
            old_name='english_at_home',
            new_name='englishAtHome',
        ),
        migrations.RenameField(
            model_name='mechtaskstudentsample',
            old_name='expect_bachelors',
            new_name='expectBachelors',
        ),
        migrations.RenameField(
            model_name='mechtaskstudentsample',
            old_name='father_bachelors',
            new_name='fatherBachelors',
        ),
        migrations.RenameField(
            model_name='mechtaskstudentsample',
            old_name='father_born_us',
            new_name='fatherBornUS',
        ),
        migrations.RenameField(
            model_name='mechtaskstudentsample',
            old_name='father_hs',
            new_name='fatherHS',
        ),
        migrations.RenameField(
            model_name='mechtaskstudentsample',
            old_name='father_work',
            new_name='fatherWork',
        ),
        migrations.RenameField(
            model_name='mechtaskstudentsample',
            old_name='minutes_per_week_english',
            new_name='minutesPerWeekEnglish',
        ),
        migrations.RenameField(
            model_name='mechtaskstudentsample',
            old_name='mother_bachelors',
            new_name='motherBachelors',
        ),
        migrations.RenameField(
            model_name='mechtaskstudentsample',
            old_name='mother_born_us',
            new_name='motherBornUS',
        ),
        migrations.RenameField(
            model_name='mechtaskstudentsample',
            old_name='mother_hs',
            new_name='motherHS',
        ),
        migrations.RenameField(
            model_name='mechtaskstudentsample',
            old_name='mother_work',
            new_name='motherWork',
        ),
        migrations.RenameField(
            model_name='mechtaskstudentsample',
            old_name='pre_school',
            new_name='preschool',
        ),
        migrations.RenameField(
            model_name='mechtaskstudentsample',
            old_name='public_school',
            new_name='publicSchool',
        ),
        migrations.RenameField(
            model_name='mechtaskstudentsample',
            old_name='race_eth',
            new_name='raceeth',
        ),
        migrations.RenameField(
            model_name='mechtaskstudentsample',
            old_name='read_30_mins_a_day',
            new_name='read30MinsADay',
        ),
        migrations.RenameField(
            model_name='mechtaskstudentsample',
            old_name='school_has_library',
            new_name='schoolHasLibrary',
        ),
        migrations.RenameField(
            model_name='mechtaskstudentsample',
            old_name='school_size',
            new_name='schoolSize',
        ),
        migrations.RenameField(
            model_name='mechtaskstudentsample',
            old_name='self_born_us',
            new_name='selfBornUS',
        ),
        migrations.RenameField(
            model_name='mechtaskstudentsample',
            old_name='students_in_english',
            new_name='studentsInEnglish',
        ),
    ]
