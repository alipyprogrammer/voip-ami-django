# Generated by Django 4.0 on 2024-01-20 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0011_rename_internal_usershamkadeh_operator_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogOnlineHamkadeh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=85)),
                ('date', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.usershamkadeh')),
            ],
        ),
    ]