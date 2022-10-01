# Generated by Django 4.0.5 on 2022-08-12 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usergroup', models.CharField(blank=True, max_length=200, null=True)),
                ('allowed_campaigns', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='usergroup',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
