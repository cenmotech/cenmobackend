# Generated by Django 4.1.7 on 2023-04-27 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='stock',
            field=models.IntegerField(default=0),
        ),
    ]