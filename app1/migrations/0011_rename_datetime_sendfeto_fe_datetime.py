# Generated by Django 4.0.5 on 2022-09-29 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_loginhistory_missedcall_remove_logdata_fe_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sendfeto',
            old_name='datetime',
            new_name='fe_datetime',
        ),
    ]
