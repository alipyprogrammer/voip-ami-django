# Generated by Django 4.0 on 2024-01-23 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0011_rename_internal_usershamkadeh_operator_number_and_more'),
        ('record', '0002_remove_logonlinehamkadeh_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voiplogonlinehamkadeh',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='User.usershamkadeh'),
        ),
    ]
