# Generated by Django 4.0 on 2024-01-28 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0012_user_statususerhamkadeh'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='StatusUserHamkadeh',
            new_name='statusUserHamkadeh',
        ),
    ]
