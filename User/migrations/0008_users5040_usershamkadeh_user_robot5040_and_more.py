# Generated by Django 4.0 on 2024-01-20 13:07

import User.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0007_user_isforward5040_user_isforwardhamkadeh_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users5040',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idd', models.CharField(max_length=85)),
                ('internal', models.CharField(blank=True, max_length=11, null=True)),
                ('name', models.CharField(max_length=85)),
                ('image', models.ImageField(blank=True, null=True, upload_to=User.models.upload_User_image_path_5040)),
            ],
        ),
        migrations.CreateModel(
            name='UsersHamkadeh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idd', models.CharField(max_length=85)),
                ('internal', models.CharField(blank=True, max_length=11, null=True)),
                ('name', models.CharField(max_length=85)),
                ('image', models.ImageField(blank=True, null=True, upload_to=User.models.upload_User_image_path_hamkadeh)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='robot5040',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='robotHamkadeh',
            field=models.BooleanField(default=False),
        ),
    ]