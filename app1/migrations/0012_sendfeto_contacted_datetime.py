# Generated by Django 4.0.5 on 2022-09-29 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0011_rename_datetime_sendfeto_fe_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='sendfeto',
            name='contacted_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
