# Generated by Django 4.0 on 2024-01-28 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0013_rename_statususerhamkadeh_user_statususerhamkadeh'),
    ]

    operations = [
        migrations.AddField(
            model_name='users5040',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='usershamkadeh',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]