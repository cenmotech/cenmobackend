# Generated by Django 4.1.7 on 2023-04-27 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0002_goods_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='stock',
            field=models.IntegerField(default=1),
        ),
    ]
