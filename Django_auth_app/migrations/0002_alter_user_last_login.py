# Generated by Django 5.1.5 on 2025-02-28 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Django_auth_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
