# Generated by Django 4.0.5 on 2022-08-22 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_alter_personaldetails_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='SMSUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('smsid', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('smstype', models.CharField(blank=True, max_length=100, null=True)),
                ('file', models.FileField(null=True, upload_to='')),
                ('count', models.BigIntegerField(blank=True, null=True)),
                ('entry', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SMSDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.CharField(blank=True, max_length=100, null=True)),
                ('Date', models.DateField(blank=True, null=True)),
                ('loan_account_no', models.CharField(blank=True, max_length=100, null=True)),
                ('amount', models.CharField(blank=True, max_length=100, null=True)),
                ('agency_name', models.CharField(blank=True, max_length=100, null=True)),
                ('response', models.CharField(blank=True, max_length=100, null=True)),
                ('smsty', models.CharField(blank=True, max_length=100, null=True)),
                ('sms', models.CharField(blank=True, max_length=1000, null=True)),
                ('entry', models.DateField(blank=True, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.smsupload')),
            ],
        ),
    ]
