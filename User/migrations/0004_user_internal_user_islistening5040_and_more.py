# Generated by Django 4.0 on 2023-10-21 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_user_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='internal',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='isListening5040',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='isListeningHamkadeh',
            field=models.BooleanField(default=False),
        ),
    ]
