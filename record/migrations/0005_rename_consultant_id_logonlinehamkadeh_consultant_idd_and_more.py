# Generated by Django 4.0 on 2024-01-28 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0004_reservationshamkadeh'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logonlinehamkadeh',
            old_name='consultant_id',
            new_name='consultant_idd',
        ),
        migrations.RenameField(
            model_name='logonlinehamkadeh',
            old_name='support_id',
            new_name='support_idd',
        ),
    ]
